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

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
| --------- | ------ | ----- | ----- | ----- | ----- | ----- | ------- |
| 1.        |        |       |       |       |       |       |         |
| 2.        |        |       |       |       |       |       |         |
| 3.        |        |       |       |       |       |       |         |
| 4.        |        |       |       |       |       |       |         |
| 5.        |        |       |       |       |       |       |         |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->

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
