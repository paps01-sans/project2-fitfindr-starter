#!/usr/bin/env python3
"""
FitFindr over HTTP. ← UNIT 9

    python serve.py                       run it on your machine
    gunicorn serve:app                    run it the way a host runs it

Everything else in this repo exits after one command. A host has nothing to
keep running, so a command line cannot be deployed. This file is the smallest
thing that can: it starts a web server, waits, and hands each request to the
same `run_agent()` your CLI calls. **No new agent logic lives here.** If your
loop works from `python app.py ask`, it works from here; if it doesn't, fix it
there, not in this file.

Two routes:

    POST /ask       {"query": "vintage graphic tee under $30",
                     "wardrobe": {...}}     ← wardrobe is optional
    GET  /health    is it awake?

`/ask` returns the session dict from `run_agent()` as JSON, unchanged — the
same keys you print from the command line, including `error`. Read
`session["error"]` first, exactly as you do everywhere else.

It runs **one request at a time**, and one route is deliberately slower than a
web server has to be. The reason is worth reading before you deploy: see the
note above `_one_at_a_time` below — it also decides which gunicorn worker you
can use.

Every `/ask` run and rejected request is appended to
`results/instrumentation.jsonl` with named fields for input, output, duration,
status, outcome, failure step, model calls, and token counts.
"""

import os
import sys
import threading
import time
import uuid
import json
from datetime import datetime, timezone

# config first, and before anything that talks to the model: it loads your .env
# and fixes the Windows console encoding for every module that imports it.
import config  # noqa: F401

from flask import Flask, jsonify, render_template, request

from agent import run_agent
from utils.data_loader import get_example_wardrobe

app = Flask(__name__)

RUN_LOG = config.RESULTS_DIR / "instrumentation.jsonl"


def write_run_log(record: dict) -> None:
    """Append one structured run record for local or hosted execution."""
    config.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with RUN_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")


# ── one request at a time ─────────────────────────────────────────────────────
# Here's why this exists.
#
# A web server will happily run two requests at once. Two things in this repo
# assume otherwise:
#
#   • If you moved a tool onto MCP in unit 4, `mcp_client.call_tool` starts
#     `mcp_server.py` as a separate process over stdio, one per call. Two
#     overlapping requests means two extra Python interpreters, and the free
#     tier you're deploying to has 512 MB for all of it. That is the reason
#     that would still be here even if everything else were perfect.
#   • `generate.py`'s pacing window and its call counter are plain module
#     globals — deliberately, because that file is teaching pacing and quota,
#     not locking. Two threads sharing them means the per-minute limiter is
#     counting something that isn't true.
#
# What the lock covers is exactly the agent run: the part that spawns
# processes and calls the model. Reading the request, rejecting a bad one, and
# turning the answer into JSON all happen outside it — so a request with a
# malformed body comes straight back with a 400 instead of queueing behind
# somebody else's agent.
#
# Serialising the runs costs you nothing here — this is one user asking one
# question — and it keeps the deployed behaviour identical to the CLI's. When
# that stops being an acceptable trade, the fix is a real queue, not a bigger
# lock.
#
# The same constraint decides your start command, and this is the part that
# bites in deployment rather than on your machine. `mcp_client.call_tool`
# wraps `asyncio.run()`, and `asyncio.run()` refuses to start when an event
# loop is already running. An async worker always has one running. So under
# `gunicorn -k gevent` (or `-k eventlet`, or `serve:app` wrapped for an ASGI
# server like uvicorn) EVERY MCP call fails with "asyncio.run() cannot be
# called from a running event loop" — not some of them under load, all of
# them, every time, in a place your laptop never showed you.
#
#     gunicorn serve:app              ← right: the DEFAULT sync worker
#     gunicorn -k gevent serve:app    ← breaks every MCP call you make

_one_at_a_time = threading.Lock()


@app.get("/")
def index():
    """Serve the browser extension."""
    return render_template("index.html")


@app.get("/health")
def health():
    """Is the server awake? A host pings something like this to find out."""
    return jsonify({"status": "ok"})


@app.post("/ask")
def ask():
    """
    Run the agent on one query.

    In:   {"query": "...", "wardrobe": {...}}   wardrobe optional — leave it
                                                out and you get the same
                                                example wardrobe the CLI uses.
    Out:  the session dict from run_agent(), as JSON.
    """
    started = time.perf_counter()
    request_id = uuid.uuid4().hex[:12]
    payload = request.get_json(silent=True) or {}
    query = (payload.get("query") or "").strip()
    if not query:
        # 400 rather than a stack trace: the caller can act on this one.
        error = "Send JSON with a 'query' field, e.g. " \
                '{"query": "vintage graphic tee under $30"}'
        write_run_log({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request_id": request_id,
            "input": payload,
            "output": {"error": error},
            "duration_ms": round((time.perf_counter() - started) * 1000, 2),
            "status": 400,
            "outcome": "rejected_input",
            "failed_step": "request_validation",
        })
        return jsonify({"error": error}), 400

    wardrobe = payload.get("wardrobe")
    if not isinstance(wardrobe, dict):
        wardrobe = get_example_wardrobe()

    # A queued request should look like a queued request. Without this the
    # second caller just sits there, and "slow" and "waiting its turn" are
    # indistinguishable from the outside — which is how people conclude the
    # deployment is broken when it is behaving exactly as designed.
    #
    # This wait notice is separate from the structured JSONL run record.
    # It says only that this request had to wait. `locked()` can be a moment out of date,
    # so the note is occasionally missed — which costs nothing, because
    # nothing depends on it.
    if _one_at_a_time.locked():
        print(
            "  [serve] another request is still running. This one is waiting "
            "its turn — serve.py handles one at a time, on purpose.",
            file=sys.stderr,
            flush=True,
        )

    failure = None
    session = None
    from generate import call_count, token_counts

    calls_before = call_count()
    tokens_before = token_counts()
    with _one_at_a_time:
        try:
            session = run_agent(query, wardrobe)
        except Exception as exc:  # noqa: BLE001 — a 500 with a sentence beats a hang
            failure = f"{type(exc).__name__}: {exc}"

    # Outside the lock: building a response is not work the next caller should
    # be waiting on.
    duration_ms = round((time.perf_counter() - started) * 1000, 2)
    calls_after = call_count()
    tokens_after = token_counts()
    if failure is not None:
        output = {"error": failure}
        status = 500
        outcome = "server_error"
        failed_step = "run_agent"
    else:
        output = {
            "error": session["error"],
            "search_count": len(session["search_results"]),
            "selected_item_id": (
                session["selected_item"].get("id")
                if session["selected_item"] else None
            ),
            "selected_item_title": (
                session["selected_item"].get("title")
                if session["selected_item"] else None
            ),
            "has_outfit": bool(session["outfit_suggestion"]),
            "has_fit_card": bool(session["fit_card"]),
            "failed_step": session.get("failed_step"),
        }
        status = 200
        outcome = "no_match" if not session["search_results"] else "success"
        failed_step = session.get("failed_step")

    write_run_log({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": request_id,
        "input": {"query": query, "wardrobe_item_count": len(wardrobe.get("items", []))},
        "output": output,
        "duration_ms": duration_ms,
        "status": status,
        "outcome": outcome,
        "failed_step": failed_step,
        "model_calls": calls_after - calls_before,
        "prompt_tokens": tokens_after["prompt"] - tokens_before["prompt"],
        "output_tokens": tokens_after["output"] - tokens_before["output"],
    })

    if failure is not None:
        return jsonify({"error": failure}), status

    return jsonify(session)


if __name__ == "__main__":
    # PORT and 0.0.0.0 are not decoration. A host tells you which port to
    # listen on through PORT, and it reaches your process from outside the
    # container — bind 127.0.0.1 and nothing but the container itself can
    # connect, which looks exactly like a broken app from the browser.
    port = int(os.getenv("PORT", "5000"))

    # Never on by default. Flask's debugger executes code typed into a browser,
    # and a deployed app with it on is a stranger's shell. Set AI201_DEBUG=1 in
    # your own terminal when you want the reloader.
    debug = os.getenv("AI201_DEBUG", "0") == "1"

    print(f"\nFitFindr is listening on http://localhost:{port}")
    print("It runs one request at a time — a second one waits for the first.")
    print("Ask it something (single quotes, as always):\n")
    print(
        f"  curl -X POST http://localhost:{port}/ask \\\n"
        f"    -H 'Content-Type: application/json' \\\n"
        f"    -d '{{\"query\": \"vintage graphic tee under $30\"}}'\n"
    )
    print("Ctrl-C to stop.\n")

    app.run(host="0.0.0.0", port=port, debug=debug)
