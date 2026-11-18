# Capstone Milestone 5 — Three Trials

- Produced by: `run_capstone_tests.py::main`
- Tested: 2026-11-18T16:28:29.436937
- Cache: disabled

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| C1. Browser search renders full result set | 4/5 | PASS (5/5) | PASS (5/5) | PASS (5/5) | MET |
| C2. Wardrobe edits survive reload | 5/5 | PASS (5/5) | PASS (5/5) | PASS (5/5) | MET |
| C3. Saved listings and sharing preserve the fit | 4/5 | PASS (5/5) | PASS (5/5) | PASS (5/5) | MET |
| C4. Rejected input is logged | 5/5 | PASS (5/5) | PASS (5/5) | PASS (5/5) | MET |
| C5. Price comparison is visible | 4/5 | PASS (5/5) | PASS (5/5) | PASS (5/5) | MET |

## Real output

### C1. Browser search renders full result set

```json
{
  "passes": 5,
  "target": 4,
  "details": [
    {
      "query": "vintage graphic tee under $30",
      "status": 200,
      "pass": true,
      "search_count": 10
    },
    {
      "query": "denim jacket under $50",
      "status": 200,
      "pass": true,
      "search_count": 7
    },
    {
      "query": "90s track jacket in size M",
      "status": 200,
      "pass": true,
      "search_count": 4
    },
    {
      "query": "silk slip dress in midi length under $40",
      "status": 200,
      "pass": true,
      "search_count": 10
    },
    {
      "query": "platform sneakers size 8",
      "status": 200,
      "pass": true,
      "search_count": 1
    }
  ]
}
```

### C2. Wardrobe edits survive reload

```json
{
  "passes": 5,
  "target": 5,
  "details": {
    "add item": true,
    "edit item": true,
    "remove item": true,
    "reload persistence": true,
    "ask payload": true
  }
}
```

### C3. Saved listings and sharing preserve the fit

```json
{
  "passes": 5,
  "target": 4,
  "details": {
    "lst_002": true,
    "lst_007": true,
    "lst_004": true,
    "lst_013": true,
    "lst_019": true
  }
}
```

### C4. Rejected input is logged

```json
{
  "passes": 5,
  "target": 5,
  "details": [
    {
      "payload": null,
      "status": 400,
      "pass": true
    },
    {
      "payload": {},
      "status": 400,
      "pass": true
    },
    {
      "payload": {
        "query": ""
      },
      "status": 400,
      "pass": true
    },
    {
      "payload": {
        "query": "   "
      },
      "status": 400,
      "pass": true
    },
    {
      "payload": {
        "query": null
      },
      "status": 400,
      "pass": true
    }
  ],
  "log_entries_added": 5
}
```

### C5. Price comparison is visible

```json
{
  "passes": 5,
  "target": 4,
  "details": [
    {
      "query": "vintage graphic tee under $30",
      "status": "compared",
      "pass": true,
      "comparison": {
        "status": "compared",
        "listing_price": 18.0,
        "average_comparable_price": 22.0,
        "difference": -4.0,
        "verdict": "below average",
        "comparable_count": 14
      }
    },
    {
      "query": "denim jacket under $50",
      "status": "compared",
      "pass": true,
      "comparison": {
        "status": "compared",
        "listing_price": 42.0,
        "average_comparable_price": 44.29,
        "difference": -2.29,
        "verdict": "below average",
        "comparable_count": 7
      }
    },
    {
      "query": "90s track jacket in size M",
      "status": "compared",
      "pass": true,
      "comparison": {
        "status": "compared",
        "listing_price": 45.0,
        "average_comparable_price": 45.67,
        "difference": -0.67,
        "verdict": "fairly priced",
        "comparable_count": 6
      }
    },
    {
      "query": "silk slip dress in midi length under $40",
      "status": "compared",
      "pass": true,
      "comparison": {
        "status": "compared",
        "listing_price": 30.0,
        "average_comparable_price": 31.86,
        "difference": -1.86,
        "verdict": "fairly priced",
        "comparable_count": 7
      }
    },
    {
      "query": "platform sneakers size 8",
      "status": "compared",
      "pass": true,
      "comparison": {
        "status": "compared",
        "listing_price": 48.0,
        "average_comparable_price": 37.5,
        "difference": 10.5,
        "verdict": "above average",
        "comparable_count": 2
      }
    }
  ],
  "surfaces_visible": true
}
```
