# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

FitFindr lets a user describe a thrift item they want, including a size and
maximum price. It searches the listings data, chooses a matching item, and
uses the user's wardrobe to suggest an outfit. It then turns the outfit idea
into a short fit card caption. If the search finds nothing, it stops early and
tells the user what they can change. As a stretch feature, it also compares the
selected item's price with similar listings.

---

## The Shape

**System:** FitFindr, the existing thrift-listing search and outfit-recommendation agent.

**Shape:** C — Extend one capability. I am adding an interactive browser
workspace for the agent: a user can submit natural-language queries with size
and budget filters, inspect every returned listing and price comparison, edit
a wardrobe in the browser, save listings, and copy or share a generated fit
card. The extension is the end-to-end browser capability over the existing
`POST /ask` run path; the agent, MCP search, listing data, and recommendation
logic stay in place rather than being rebuilt.

**Out of scope:** I am not adding accounts or server-side favorites; I am not
adding database persistence or live marketplace scraping; and I am not
replacing Flask or rebuilding the agent in React/Next.js. The MVP remains
database-free with `localStorage`, and alternate-listing outfit re-runs stay
out unless a later milestone has time. The core browser implementation is
small enough to fit the ninety-minute build limit before deployment and
testing.

---

## Instrumentation

Every `/ask` run and malformed `/ask` request is appended to
`results/instrumentation.jsonl`. Each JSON line contains a UTC timestamp,
request ID, input summary, output summary, duration, HTTP status, outcome,
failed step, model-call count, prompt tokens, and output tokens.

```text
{"timestamp":"2026-11-18T20:46:07.170655+00:00","request_id":"22746863bb71","input":{"query":"vintage graphic tee under","wardrobe_item_count":10},"output":{"search_count":10,"selected_item_id":"lst_002","selected_item_title":"Y2K Baby Tee — Butterfly Print","has_fit_card":true,"failed_step":"suggest_outfit"},"duration_ms":13715.35,"status":200,"outcome":"success","failed_step":"suggest_outfit","model_calls":0,"prompt_tokens":0,"output_tokens":0}
{"timestamp":"2026-11-18T20:46:17.144704+00:00","request_id":"337d3a6280b0","input":{"query":"denim jacket under","wardrobe_item_count":10},"output":{"search_count":9,"selected_item_id":"lst_007","selected_item_title":"Denim Jacket — Light Wash, Cropped","has_fit_card":true,"failed_step":"suggest_outfit"},"duration_ms":7939.6,"status":200,"outcome":"success","failed_step":"suggest_outfit","model_calls":0,"prompt_tokens":0,"output_tokens":0}
{"timestamp":"2026-11-18T20:46:28.933370+00:00","request_id":"6b80b64f0729","input":{"query":"90s track jacket in size M","wardrobe_item_count":10},"output":{"search_count":4,"selected_item_id":"lst_004","selected_item_title":"90s Track Jacket — Navy/White Stripe","has_fit_card":true,"failed_step":"suggest_outfit"},"duration_ms":9740.77,"status":200,"outcome":"success","failed_step":"suggest_outfit","model_calls":0,"prompt_tokens":0,"output_tokens":0}
{"timestamp":"2026-11-18T20:46:38.892235+00:00","request_id":"809bfa787fe5","input":{"query":"silk slip dress in midi length under","wardrobe_item_count":10},"output":{"search_count":10,"selected_item_id":"lst_013","selected_item_title":"90s Silk Slip Dress — Floral, Midi Length","has_fit_card":true,"failed_step":"suggest_outfit"},"duration_ms":7922.51,"status":200,"outcome":"success","failed_step":"suggest_outfit","model_calls":0,"prompt_tokens":0,"output_tokens":0}
{"timestamp":"2026-11-18T20:46:48.647752+00:00","request_id":"413ae9a4f0c1","input":{"query":"platform sneakers size 8","wardrobe_item_count":10},"output":{"search_count":1,"selected_item_id":"lst_019","selected_item_title":"Platform Sneakers — White Chunky Sole","has_fit_card":true,"failed_step":"suggest_outfit"},"duration_ms":7731.59,"status":200,"outcome":"success","failed_step":"suggest_outfit","model_calls":0,"prompt_tokens":0,"output_tokens":0}
{"timestamp":"2026-11-18T20:46:57.831495+00:00","request_id":"e2f7d245a072","input":{"query":"graphic tee under","wardrobe_item_count":10},"output":{"search_count":6,"selected_item_id":"lst_017","selected_item_title":"Mesh Long-Sleeve Top — Black","has_fit_card":true,"failed_step":"suggest_outfit"},"duration_ms":7150.59,"status":200,"outcome":"success","failed_step":"suggest_outfit","model_calls":0,"prompt_tokens":0,"output_tokens":0}
{"timestamp":"2026-11-18T20:47:06.054991+00:00","request_id":"6163f49a8d4c","input":{"query":"corduroy pants under","wardrobe_item_count":10},"output":{"search_count":3,"selected_item_id":"lst_005","selected_item_title":"Corduroy Wide-Leg Pants — Rust","has_fit_card":true,"failed_step":"suggest_outfit"},"duration_ms":6163.49,"status":200,"outcome":"success","failed_step":"suggest_outfit","model_calls":0,"prompt_tokens":0,"output_tokens":0}
{"timestamp":"2026-11-18T20:47:13.924787+00:00","request_id":"ce652afb033e","input":{"query":"knit cardigan under","wardrobe_item_count":10},"output":{"search_count":3,"selected_item_id":"lst_008","selected_item_title":"Knit Cardigan — Chunky Brown","has_fit_card":true,"failed_step":"suggest_outfit"},"duration_ms":5837.77,"status":200,"outcome":"success","failed_step":"suggest_outfit","model_calls":0,"prompt_tokens":0,"output_tokens":0}
{"timestamp":"2026-11-18T20:47:20.690954+00:00","request_id":"4b54f42d2bf0","input":{"query":"flannel shirt size XL","wardrobe_item_count":10},"output":{"search_count":1,"selected_item_id":"lst_003","selected_item_title":"Oversized Flannel Shirt — Plaid Red/Black","has_fit_card":true,"failed_step":"suggest_outfit"},"duration_ms":4717.19,"status":200,"outcome":"success","failed_step":"suggest_outfit","model_calls":0,"prompt_tokens":0,"output_tokens":0}
{"timestamp":"2026-11-18T20:47:28.156136+00:00","request_id":"1760658dcccf","input":{"query":"brown boots under","wardrobe_item_count":10},"output":{"search_count":6,"selected_item_id":"lst_008","selected_item_title":"Knit Cardigan — Chunky Brown","has_fit_card":true,"failed_step":"suggest_outfit"},"duration_ms":5400.04,"status":200,"outcome":"success","failed_step":"suggest_outfit","model_calls":0,"prompt_tokens":0,"output_tokens":0}
```

**One rejected run**

```text
{"timestamp":"2026-11-18T20:48:30.951855+00:00","request_id":"3b14cdfa1688","input":{},"output":{"error":"Send JSON with a 'query' field"},"duration_ms":0.14,"status":400,"outcome":"rejected_input","failed_step":"request_validation","model_calls":0,"prompt_tokens":0,"output_tokens":0}
```

The failed run is a malformed request with no `query`. It was returned as HTTP
400 and written to the JSONL log instead of disappearing.

## What It Costs

I measured one complete `/ask` run by sending ten uncached matching requests to
the local Flask server, with `AI201_CACHE=0`, and averaging the server-measured
`duration_ms` field. The mean was **7.632 seconds per run**, with a median of
**7.441 seconds**. The measured range was **4.717 to 13.715 seconds**. This
measurement includes MCP search-process startup and fallback handling. No model
calls or tokens were measured because the current API key is rejected, so
these runs produced **0 model calls and 0 tokens**. This is a real measured
runtime cost, not a cost estimate from a pricing page.

For one run: **7.632 seconds** of compute. For 100 people in one day, assuming
one run per person: `100 runs × 7.632 seconds/run = 763.2 seconds`, or about
**12.72 minutes** of compute. This is not a dollar-cost estimate because I did
not complete a paid or authenticated model run; it measures local wall-clock
cost and MCP startup rather than API charges.

---

## Capstone

### How I Used AI

For this capstone, I used Copilot as a coding assistant rather than as a
replacement for my own decisions. I first asked it to organize the project
scope into Shape C and to identify a browser extension that could reuse the
existing `/ask` run path. I reviewed that plan, kept the database-free
localStorage design, and cut account features and live marketplace scraping
before implementation.

When the feedback pointed out that query parsing was too tightly mixed into
`run_agent()`, I directed Copilot to extract `parse_query()` and separate
model-dependent calls from the deterministic price comparison. I tested those
changes with my own terminal commands and kept the parts that showed real
results. I also used it to generate an initial outline for the structured log
and test runner, then inspected and ran the code myself.

Copilot found the missing saved-listing implementation in the Milestone 5
diagnosis, and I used that diagnosis to implement Save/Unsave, a saved panel,
Copy Caption, and Share Fit. I did not assume the improvement worked: I reran
the full three-trial set and recorded both the missing and passing evidence.
The final write-up reflects the measured outcomes, including the limitations
of a local run and a rejected API key.

## Capstone Milestone 5 — Run Log

`run_capstone_tests.py::main` ran the five capstone criteria three times each,
with `config.CACHE_ENABLED=False`. The generated machine-readable report is
`results/run_capstone_milestone5.md`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| C1. Browser search renders full result set | 4/5 | PASS (5/5) | PASS (5/5) | PASS (5/5) | MET |
| C2. Wardrobe edits survive reload | 5/5 | PASS (5/5) | PASS (5/5) | PASS (5/5) | MET |
| C3. Saved listings and sharing preserve the fit | 4/5 | FAIL (0/5) | FAIL (0/5) | FAIL (0/5) | MISSED |
| C4. Rejected input is logged | 5/5 | PASS (5/5) | PASS (5/5) | PASS (5/5) | MET |
| C5. Price comparison is visible | 4/5 | PASS (5/5) | PASS (5/5) | PASS (5/5) | MET |

**Before improvement — Verdicts**

- C1 — MET: 5/5 matching browser searches returned and rendered results in
  each of three trials.
- C2 — MET: the add/edit/remove, reload-persistence, and `/ask` payload checks
  passed 5/5 in each trial.
- C3 — MISSED: 0/5 save/share checks passed in each trial. The stage was the
  browser presentation layer: result and recommendation views had no
  saved-listing state or copy/share actions. The mechanism was missing
  implementation, not a bug in search or session data.
- C4 — MET: all five malformed payload variants returned 400 and logged once
  in each trial.
- C5 — MET: price comparison was produced and visible in all five checked
  searches in each trial.

### Real output for C1 — Browser search

Produced by `run_capstone_tests.py::c1_search_trial`, calling
`serve.py::ask` and `agent.py::run_agent`:

```json
{"query":"vintage graphic tee under $30","status":200,"pass":true,"search_count":10}
{"query":"denim jacket under $50","status":200,"pass":true,"search_count":7}
{"query":"90s track jacket in size M","status":200,"pass":true,"search_count":4}
{"query":"silk slip dress in midi length under $40","status":200,"pass":true,"search_count":10}
{"query":"platform sneakers size 8","status":200,"pass":true,"search_count":1}
```

### Real output for C2 — Wardrobe persistence

Produced by `run_capstone_tests.py::c2_wardrobe_trial`, checking
`static/app.js` and `templates/index.html`:

```json
{"add item":true,"edit item":true,"remove item":true,"reload persistence":true,"ask payload":true}
```

### Real output for C3 — Saved listings and sharing

Produced by `run_capstone_tests.py::c3_saved_share_trial`, checking
`static/app.js` and `templates/index.html`:

```json
{"lst_002":false,"lst_007":false,"lst_004":false,"lst_013":false,"lst_019":false}
```

This run found the feature absent: no saved-localStorage key, save action,
saved panel, copy-caption action, or Web Share implementation exists in the
browser code.

### Real output for C4 — Rejected input

Produced by `run_capstone_tests.py::c4_rejected_trial`, calling
`serve.py::ask`:

```json
{"payload":null,"status":400,"pass":true}
{"payload":{},"status":400,"pass":true}
{"payload":{"query":""},"status":400,"pass":true}
{"payload":{"query":"   "},"status":400,"pass":true}
{"payload":{"query":null},"status":400,"pass":true}
```

### Real output for C5 — Price comparison

Produced by `run_capstone_tests.py::c5_price_trial`, calling
`agent.py::run_agent` and `tools.py::compare_price`:

```json
{"listing":"Y2K Baby Tee","status":"compared","average":22.0,"difference":-4.0,"verdict":"below average","count":14}
{"listing":"Denim Jacket","status":"compared","average":44.29,"difference":-2.29,"verdict":"below average","count":7}
{"listing":"90s Track Jacket","status":"compared","average":45.67,"difference":-0.67,"verdict":"fairly priced","count":6}
{"listing":"Silk Slip Dress","status":"compared","average":31.86,"difference":-1.86,"verdict":"fairly priced","count":7}
{"listing":"Platform Sneakers","status":"compared","average":37.5,"difference":10.5,"verdict":"above average","count":2}
```

### Improvement and After Run

**The improvement:** I added the saved-listings and sharing layer only.

The change adds `fitfindr-saved-listings` persistence, Save/Unsave controls on
result cards, a saved-listings panel that survives reloads, Copy Caption, and
Share Fit using the browser Share API with a clipboard fallback.

**Which miss it fixes:** C3 — the browser had no save/share implementation.
The missed stage was rendering and interaction, not the agent. The fix binds
saved IDs to existing listing cards and reconstructs the share text from the
current selected listing, outfit suggestion, and fit card.

**After run — three trials**

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| C1. Browser search renders full result set | 4/5 | PASS (5/5) | PASS (5/5) | PASS (5/5) | MET |
| C2. Wardrobe edits survive reload | 5/5 | PASS (5/5) | PASS (5/5) | PASS (5/5) | MET |
| C3. Saved listings and sharing preserve the fit | 4/5 | PASS (5/5) | PASS (5/5) | PASS (5/5) | MET |
| C4. Rejected input is logged | 5/5 | PASS (5/5) | PASS (5/5) | PASS (5/5) | MET |
| C5. Price comparison is visible | 4/5 | PASS (5/5) | PASS (5/5) | PASS (5/5) | MET |

Real output for C3 after the improvement:

```json
{"lst_002":true,"lst_007":true,"lst_004":true,"lst_013":true,"lst_019":true}
```

**Did it help:** C3 changed from MISSED (0/5 in all three trials) to MET
(5/5 in all three trials). C1, C2, C4, and C5 remained MET. No worse behavior
was observed in this test set. The tradeoff is that saved items are
browser-local; they do not sync across devices or survive browser storage
clearing, which is intentional for the database-free MVP scope.

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Searches the listings data for description keywords, an optional size, and an optional inclusive price limit.
- **Inputs:** `description` (str), `size` (str | None), and `max_price` (float | None). A size matches a case-insensitive size token in the listing, so `M` matches `S/M` but not `XL` or `US 9`.
- **Returns:** A list of listing dicts, sorted with the best keyword match first. Each dict includes `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`.
- **When it has nothing:** Returns an empty list `[]`, not `None` or an exception.

### `suggest_outfit`

- **What it does:** Suggests one or two outfits that use the new listing and pieces from the user's wardrobe.
- **Inputs:** `new_item` (dict) and `wardrobe` (dict with an `items` list of wardrobe item dicts).
- **Returns:** A non-empty string containing outfit suggestions and naming wardrobe pieces when the wardrobe has items.
- **When it has nothing:** If the wardrobe has no items, returns a non-empty string with general styling advice for the new item.

### `create_fit_card`

- **What it does:** Writes a short social media caption for the selected item and its suggested outfit.
- **Inputs:** `outfit` (str) and `new_item` (dict).
- **Returns:** A two-to-four sentence string that mentions the item, price, platform, and outfit vibe.
- **When it has nothing:** If `outfit` is empty or only whitespace, returns a descriptive message instead of calling the model.

### `compare_price` (stretch feature)

- **What it does:** Compares a selected listing's price with similar listings in the same category that share at least one style tag.
- **Inputs:** `new_item` (dict) with `id`, `category`, `style_tags`, and numeric `price` fields.
- **Returns:** A dict containing the listing price, average comparable price, price difference, verdict (`below average`, `fairly priced`, or `above average`), and comparable count.
- **When it has nothing:** Returns a dict with `status` set to `unavailable`, a message, the listing price, and a comparable count of `0`.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If `search_listings` returns an empty list, put a message in `session["error"]` that tells the user what to change and stop before calling `suggest_outfit`. Otherwise, put the first result in `session["selected_item"]` and pass it to `suggest_outfit`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** A regular expression extracts an optional dollar amount after `under` or `below`, and an optional size after `size` or `in size`. The remaining words become the description.

**What moves through the session:** The query is parsed into `session["parsed"]`, then the results go into `session["search_results"]`. The first result moves into `session["selected_item"]`, then goes to `compare_price` and its result goes into `session["price_comparison"]`. The selected item and `session["wardrobe"]` then go to `suggest_outfit`. Its string goes into `session["outfit_suggestion"]`, then moves with the selected item into `create_fit_card`, whose result goes into `session["fit_card"]`.

Someone else could build these tools from this spec because the input types, output fields, size matching rule, empty cases, query parsing, and session handoffs are defined.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '...'

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print([(x['id'], x['price']) for x in search_listings('graphic tee', max_price=30)])"
[('lst_002', 18.0), ('lst_006', 24.0), ('lst_017', 15.0), ('lst_033', 19.0), ('lst_011', 27.0), ('lst_015', 26.0)]
```

```
$ python -c "import tools; from utils.data_loader import load_listings, get_example_wardrobe; tools.generate=lambda prompt, **kwargs: 'OUTFIT: use the white ribbed tank with the jeans'; print(tools.suggest_outfit(load_listings()[0], get_example_wardrobe()))"
OUTFIT: use the white ribbed tank with the jeans
```

```
$ python -c "import tools; from utils.data_loader import load_listings; tools.generate=lambda prompt, **kwargs: 'CAPTION: vintage denim find with a casual streetwear vibe'; print(tools.create_fit_card('jeans and white sneakers', load_listings()[0]))"
CAPTION: vintage denim find with a casual streetwear vibe
```

```
$ python -c "from tools import compare_price; from utils.data_loader import load_listings; print(compare_price(load_listings()[0]))"
{'status': 'compared', 'listing_price': 38.0, 'average_comparable_price': 27.75, 'difference': 10.25, 'verdict': 'above average', 'comparable_count': 8}
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- _What I asked for:_ I asked Copilot to help me turn the tool requirements
  into specific input, output, and empty-case rules.
- _What came back:_ We defined the listing fields, the wardrobe shape, the
  empty list result for searches, and the session values passed between tools.
- _What I changed:_ I wrote those rules into the Tool Inventory and used them
  while building the tools and planning loop.

**Moment 2**

- _What I asked for:_ I asked Claude to clarify how to compare sizes such as
  `M`, `S/M`, `XL`, and shoe sizes without using unsafe substring matching.
- _What came back:_ The clarification suggested comparing normalized size
  tokens so a requested `M` would match `S/M` but not `XL` or `US 9`.
- _What I changed:_ I added token-based size matching to `search_listings` and
  checked the empty-search branch separately from the successful path.

**Moment 3**

- _What I asked for:_ I asked Copilot to help me test the MCP move and run all
  five criteria five times with caching turned off.
- _What came back:_ The MCP search worked, the empty-search and price-limit
  criteria passed, but the model rejected the API key on every model-backed
  run.
- _What I changed:_ I added trace steps and clear failure messages, then added
  a deterministic fallback fit card when the model is unavailable. I ran the
  full test again and recorded both results instead of hiding the failures.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
| --------- | ------ | ----- | ----- | ----- | ----- | ----- | ------- |
| 1. Matching query completes all three tools | 4 of 5 | FAIL | FAIL | FAIL | FAIL | FAIL | MISSED (0/5) |
| 2. Impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected item stays consistent across tools | 5 of 5 | FAIL | FAIL | FAIL | FAIL | FAIL | MISSED (0/5) |
| 4. Fit cards include the important listing details | 4 of 5 | FAIL | FAIL | FAIL | FAIL | FAIL | MISSED (0/5) |
| 5. Search results respect the price limit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

**Criterion 1 — `results/run_2026-10-14_2135_before.md`, produced by
`run_eval.py::main` calling `agent.py::run_agent`:**

```text
- stopped early: yes — The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

[1] search_listings (via MCP)
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[2] compare_price
[3] model
      out: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.goo…
      →    model unavailable: stopping with an actionable message
```

**Criterion 2 — `results/run_2026-10-14_2135_before.md`, produced by
`run_eval.py::main` calling `agent.py::run_agent`:**

```text
- stopped early: yes — No listings matched. Try changing the description, size, or maximum price.
- selected_item: (none)
- search_results: 0

[1] search_listings (via MCP)
      out: [] (empty)
[2] branch
      out: No listings matched. Try changing the description, size, or maximum price.
      →    empty search: stopping before outfit tools
```

**Criterion 3 — `results/run_2026-10-14_2135_before.md`, produced by
`run_eval.py::main` calling `agent.py::run_agent`:**

```text
- stopped early: yes — The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.
- selected_item: 90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
- search_results: 4

[1] search_listings (via MCP)
      out: 4 items: 90s Track Jacket — Navy/White Stripe, 90s Leather Bomber — Black, 90s Silk Slip Dress — Floral, Midi Length … +1 more
[2] compare_price
      in:  90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
[3] model
      →    model unavailable: stopping with an actionable message
```

The handoff could not be observed because `suggest_outfit` was never reached;
the model failure stopped the run after `compare_price`.

**Criterion 4 — `results/run_2026-10-14_2135_before.md`, produced by
`run_eval.py::main` calling `agent.py::run_agent`:**

```text
- stopped early: yes — The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Fit card: (not produced)

[3] model
      out: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.goo…
      →    model unavailable: stopping with an actionable message
```

**Criterion 5 — `results/run_2026-10-14_2135_before.md`, produced by
`run_eval.py::main` calling `agent.py::run_agent`:**

```text
- Query: graphic tee under $30
- stopped early: yes — The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 6

[1] search_listings (via MCP)
      out: 6 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Mesh Long-Sleeve Top — Black … +3 more
```

The search tool returned six results on each of the five tries; the direct
MCP search check for the same `$30` limit returned prices
`18.0, 24.0, 15.0, 19.0, 27.0, and 26.0`, so every result respected the
inclusive ceiling.

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| #   | Criterion | Target | Verdict | How I decided |
| --- | --------- | ------ | ------- | ------------- |
| 1   | Matching query completes all three tools | 4 of 5 | MISSED (0/5) | All five matching runs reached MCP search and `compare_price`, but the model rejected the API key before `suggest_outfit` and `create_fit_card`, so none completed all three tools. |
| 2   | Impossible query stops before the second tool | 5 of 5 | MET (5/5) | All five impossible queries returned an empty MCP result and the trace ended at the empty-search branch before any outfit tool. |
| 3   | Selected item stays consistent across tools | 5 of 5 | MISSED (0/5 observable) | The selected item was present in all five sessions, but `suggest_outfit` was never reached because the model failed first, so the required cross-tool handoff could not be verified in any try. |
| 4   | Fit cards include the important listing details | 4 of 5 | MISSED (0/5) | No fit card was produced in any try because the first model-backed tool stopped on the rejected API key. |
| 5   | Search results respect the price limit | 5 of 5 | MET (5/5) | The MCP search returned six results in each try, and the recorded prices were all at or below the inclusive `$30` limit. |

**Diagnoses**

**Criterion 1 — MISSED:** This failed at the model step in
`agent.py::run_agent`, after the MCP `search_listings` tool and
`compare_price` had succeeded. The `generate()` adapter raised
`ModelUnavailable` because the API key was rejected, so the loop's model
handler set `session["error"]` and stopped before `suggest_outfit`; therefore
the run could not reach `create_fit_card`. This same mechanism caused all five
misses.

**Criterion 3 — MISSED:** This was not evidence that the selected item changed.
The session consistently selected the expected listing, but the failure
happened at the model step before `suggest_outfit` received `new_item`.
Because the handoff was never executed, the criterion's required comparison
between `session["selected_item"]` and the tool input was unobservable in all
five tries. The problem is the model-service failure path, not the search
branch or the session assignment.

**Criterion 4 — MISSED:** This failed at the model step before the
`create_fit_card` tool. The rejected API key caused `suggest_outfit` to raise
`ModelUnavailable`, so the loop stored an error and left
`session["fit_card"]` as `None`. Since no caption existed, it could not
contain the required title, price, platform, or two-to-four sentence format.
All five misses share this same model-output failure.

Criteria 2 and 5 were met, so there was no miss to diagnose for either one.
I did not revise any criterion: the targets were measurable and the failed
criteria were genuinely unmet or unobservable under the recorded model
failure, rather than incorrectly worded.

---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[2] compare_price
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: dict with keys: status, listing_price, average_comparable_price, difference, verdict, comparable_count
[3] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: General styling advice for the item.
[4] create_fit_card
      in:  dict with keys: outfit, new_item
      out: General styling advice for the item.

```

**Empty search**

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
[2] branch
      out: No listings matched. Try changing the description, size, or maximum price.
      →    empty search: stopping before outfit tools

```

**Failure checks**

- Empty search: `designer ballgown size XXS under $5` returned
  `No listings matched. Try changing the description, size, or maximum price.`
  and stopped before the outfit tools.
- Empty wardrobe: running with `get_empty_wardrobe()` returned
  `General styling advice for the item.` rather than crashing or returning an
  empty string.
- Model unavailable: I deliberately replaced the model adapter with a
  `ModelUnavailable` failure. The agent returned
  `The model could not be reached. Check your API key and try again.` rather
  than exposing a stack trace.

**On the MCP move:** `search_listings` is registered in `mcp_server.py` and
`agent.py::run_agent` calls it through `mcp_client.call_tool`. The MCP call
returned the same list of listing dictionaries as the direct call, and the
normal path still completed. The trace labels the call as
`search_listings (via MCP)`.

---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

I changed one place in `agent.py::run_agent`: when `ModelUnavailable` is raised,
the existing API-key error remains in `session["error"]`, but the agent now
creates deterministic fallback outfit advice and a two-sentence fit card from
the selected listing's title, price, and platform.

**Which failure it was meant to fix:**

The before run reached MCP search and `compare_price`, then stopped before
`suggest_outfit` and `create_fit_card` because the API key was rejected. The
fallback keeps the output contract usable while still telling the user the
model was unavailable.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
| --------- | ------ | ----- | ----- | ----- | ----- | ----- | ------- |
| 1. Matching query completes all three tools | 4 of 5 | FAIL | FAIL | FAIL | FAIL | FAIL | MISSED (0/5) |
| 2. Impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected item stays consistent across tools | 5 of 5 | FAIL | FAIL | FAIL | FAIL | FAIL | MISSED (0/5 observable) |
| 4. Fit cards include the important listing details | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search results respect the price limit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Did it help, and how do I know:**

Partly. Criterion 4 improved from 0/5 to 5/5 because the fallback supplied a
two-sentence fit card containing the selected title, price, and platform.
Criteria 2 and 5 stayed at 5/5, so the change did not disturb the existing
branch or price filtering. Criterion 1 remained missed because the fallback
does not make the two model tools run; it supplies replacement output after
`ModelUnavailable`. Criterion 3 remained unobservable because
`suggest_outfit` still was not called with `new_item`.

The complete after-run report is
`results/run_2026-10-15_0138_after.md`, produced by
`run_eval.py::main` with five tries per scenario and caching disabled. One
matching-criterion try recorded:

```text
- stopped early: yes — The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10
Fit card:
Y2K Baby Tee — Butterfly Print at $18.0 from depop makes an easy everyday look. Pair it with simple layers for a casual vibe.
[3] model
      →    model unavailable: using deterministic fallback content
```

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->

---

## What's Still Broken

### Capstone status

All five capstone criteria passed in the after run: C1, C2, C3, C4, and C5
each passed 5/5 in all three trials. There is no capstone criterion left
missed, so I stopped feature work rather than lowering or changing a target.
The tests are still limited: clipboard and Web Share behavior depend on browser
permissions, and the current API key was rejected, so a fully successful
model-generated outfit and fit card was not measured locally.

The targets were generally demanding enough for this MVP. C2 and C4 are strict
5/5 checks because localStorage and request validation can be observed
deterministically. C1 and C5 allow one miss out of five because network and
model fallback behavior can vary. C3 reached 5/5 after the improvement, so I
would tighten its future target to 5/5 for the save, reload, copy, and share
data fields rather than the 4/5 browser-permission target used in this run.

**What I'd do next if this were real:** I would first deploy to Render and
verify the browser, `/health`, `/ask`, and a valid model key from one public
URL, because that is the highest-risk gap between a local Flask app and a
usable service. If that worked, I would then add server-side persistence and
accounts only if cross-device saved wardrobes became an actual requirement,
because browser-only storage is intentionally sufficient for this MVP.

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->

Criterion 1 is still missed. The matching query did not complete all three
actual tool calls because the model failed before `suggest_outfit` and
`create_fit_card`. The fallback creates replacement text, but it does not count
as running those tools. I would fix this by making the model-backed tools
handle `ModelUnavailable` themselves and return their normal output shape, or
by giving them a local non-model fallback implementation. I stopped after one
improvement because the assignment asks for one measured change, and the
fallback already improved criterion 4.

Criterion 3 is still not fully verified. The selected item was set correctly,
but `suggest_outfit` never received `new_item` during the failed model runs, so
there was no real cross-tool handoff to compare. I would add a test hook or a
successful model run and then record the selected item id at the actual tool
boundary. I stopped because the API key problem prevented that observation,
and changing the evaluation to pretend the handoff happened would not be
honest.

The MCP move itself worked. `search_listings` is registered in
`mcp_server.py`, and `agent.py::run_agent` now calls it through
`mcp_client.call_tool`. The returned listing data and the price-limit behavior
matched the direct tool call, so I did not see a behavior change from moving
that tool to MCP.

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
