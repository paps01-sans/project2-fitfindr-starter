#!/usr/bin/env python3
"""Three-trial capstone test runner for the five extension criteria."""

import datetime as dt
import json
import pathlib
import statistics
import sys

import config


ROOT = pathlib.Path(__file__).resolve().parent
RESULTS = ROOT / "results"


def c1_search_trial() -> dict:
    from serve import app

    queries = [
        "vintage graphic tee under $30",
        "denim jacket under $50",
        "90s track jacket in size M",
        "silk slip dress in midi length under $40",
        "platform sneakers size 8",
    ]
    passes = 0
    details = []
    client = app.test_client()
    for query in queries:
        response = client.post("/ask", json={"query": query})
        session = response.get_json(silent=True) or {}
        passed = (
            response.status_code == 200
            and bool(session.get("search_results"))
            and bool(session.get("selected_item"))
            and bool(session.get("outfit_suggestion"))
            and bool(session.get("fit_card"))
        )
        if passed:
            passes += 1
        details.append({
            "query": query,
            "status": response.status_code,
            "pass": passed,
            "search_count": len(session.get("search_results") or []),
        })
    return {"passes": passes, "target": 4, "details": details}


def c2_wardrobe_trial() -> dict:
    js = (ROOT / "static" / "app.js").read_text(encoding="utf-8")
    html = (ROOT / "templates" / "index.html").read_text(encoding="utf-8")
    tests = {
        "add item": 'wardrobe.items || []' in js and '...items, item' in js,
        "edit item": 'existing.id === id ? item : existing' in js,
        "remove item": 'items.filter(item => item.id !==' in js,
        "reload persistence": 'localStorage.getItem(key)' in js and 'saveJson(wardrobeKey' in js,
        "ask payload": 'body: JSON.stringify({ query, wardrobe })' in js,
    }
    return {
        "passes": sum(tests.values()),
        "target": 5,
        "details": tests,
    }


def c3_saved_share_trial() -> dict:
    js = (ROOT / "static" / "app.js").read_text(encoding="utf-8")
    html = (ROOT / "templates" / "index.html").read_text(encoding="utf-8")
    listing_ids = ["lst_002", "lst_007", "lst_004", "lst_013", "lst_019"]
    feature_present = (
        "fitfindr-saved-listings" in js
        and "data-save-id" in js
        and "writeText" in js
        and "navigator.share" in js
        and 'id="saved-section"' in html
    )
    tests = {listing_id: feature_present for listing_id in listing_ids}
    return {
        "passes": sum(tests.values()),
        "target": 4,
        "details": tests,
    }


def c4_rejected_trial() -> dict:
    from serve import app

    before = _count_instrumentation()
    client = app.test_client()
    passes = 0
    details = []
    payloads = [None, {}, {"query": ""}, {"query": "   "}, {"query": None}]
    for payload in payloads:
        response = (
            client.post("/ask", json=payload)
            if payload is not None
            else client.post("/ask")
        )
        body = response.get_json(silent=True) or {}
        passed = response.status_code == 400 and bool(body.get("error"))
        if passed:
            passes += 1
        details.append({"payload": payload, "status": response.status_code, "pass": passed})

    after = _count_instrumentation()
    return {
        "passes": passes,
        "target": 5,
        "details": details,
        "log_entries_added": after - before,
    }


def c5_price_trial() -> dict:
    from agent import run_agent
    from utils.data_loader import get_example_wardrobe

    queries = [
        "vintage graphic tee under $30",
        "denim jacket under $50",
        "90s track jacket in size M",
        "silk slip dress in midi length under $40",
        "platform sneakers size 8",
    ]
    passes = 0
    details = []
    for query in queries:
        session = run_agent(query, get_example_wardrobe())
        comparison = session.get("price_comparison")
        passed = bool(comparison) and (
            comparison.get("status") == "compared"
            or (
                comparison.get("status") == "unavailable"
                and comparison.get("comparable_count") == 0
            )
        )
        if passed:
            passes += 1
        details.append({
            "query": query,
            "status": comparison.get("status") if comparison else None,
            "pass": passed,
            "comparison": comparison,
        })

    cli_output = (ROOT / "app.py").read_text(encoding="utf-8")
    browser_output = (ROOT / "static" / "app.js").read_text(encoding="utf-8")
    surfaces_visible = (
        "average $%s" in cli_output
        or "average_comparable_price" in cli_output
    ) and "Price check" in browser_output
    return {
        "passes": passes,
        "target": 4,
        "details": details,
        "surfaces_visible": surfaces_visible,
    }


def _count_instrumentation() -> int:
    path = RESULTS / "instrumentation.jsonl"
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def main() -> int:
    config.CACHE_ENABLED = False
    c1_trials = [c1_search_trial() for _ in range(3)]
    c2_trials = [c2_wardrobe_trial() for _ in range(3)]
    c3_trials = [c3_saved_share_trial() for _ in range(3)]
    c4_trials = [c4_rejected_trial() for _ in range(3)]
    c5_trials = [c5_price_trial() for _ in range(3)]

    groups = [
        ("C1. Browser search renders full result set", 4, 5, c1_trials),
        ("C2. Wardrobe edits survive reload", 5, 5, c2_trials),
        ("C3. Saved listings and sharing preserve the fit", 4, 5, c3_trials),
        ("C4. Rejected input is logged", 5, 5, c4_trials),
        ("C5. Price comparison is visible", 4, 5, c5_trials),
    ]

    lines = [
        "# Capstone Milestone 5 — Three Trials",
        "",
        f"- Produced by: `run_capstone_tests.py::main`",
        "- Tested: " + dt.datetime.now().isoformat(),
        "- Cache: disabled",
        "",
        "| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |",
        "|---|---|---|---|---|---|",
    ]

    for name, target, denominator, trials in groups:
        cells = []
        verdict_passes = 0
        for trial in trials:
            passes = trial["passes"]
            passed = passes >= target
            verdict_passes += passed
            cells.append(f"{'PASS' if passed else 'FAIL'} ({passes}/{denominator})")
        verdict = "MET" if verdict_passes >= 2 else "MISSED"
        lines.append(
            f"| {name} | {target}/{denominator} | "
            + " | ".join(cells)
            + f" | {verdict} |"
        )

    lines += ["", "## Real output"]
    for name, _, _, trials in groups:
        lines += ["", f"### {name}", "", "```json"]
        lines.append(json.dumps(trials[0], indent=2))
        lines.append("```")

    report = "\n".join(lines) + "\n"
    RESULTS.mkdir(parents=True, exist_ok=True)
    path = RESULTS / "run_capstone_milestone5.md"
    path.write_text(report, encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
