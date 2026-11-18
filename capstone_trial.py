#!/usr/bin/env python3
"""
One capstone trial against the deployed service. (Milestone 5)

    python capstone_trial.py 1          # writes results/capstone/trial1/
    python capstone_trial.py 2 --base http://localhost:5000

Every trial sends exactly the same requests in the same order, so the three
trials differ only in what the live system does. Nothing here grades anything.
It saves the raw output, and capstone_score.py grades it against criteria.md.

What one trial sends, and which criterion each part feeds:

    GET  /health                        warm-up, required by criterion 2
    POST /ask  x7 good  (GOOD[0:7])     criteria 1, 2, 4 (the first 5 are criterion 4's)
    POST /ask  x3 bad   (BAD)           criterion 1
         ...with GET /logs after each of those 10 /ask calls        criterion 3
    POST /ask  x3 good  (GOOD[7:10])    criterion 2 (10 `ok` runs in total)
    POST /ask  spares   (SPARE_GOOD)    criterion 2, only to replace a non-`ok` run
    POST /ask  x5 empty wardrobe        criterion 5
    GET  /logs?n=200                    end-of-trial snapshot of every record

Uses only the standard library, so it runs from any Python 3.11+.
"""

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://ai201-project2-fitfindr-v2026.onrender.com"
ROOT = Path(__file__).parent

# Queries that matched a listing in Milestone 3. Same list, same order, every trial.
GOOD = [
    "vintage graphic tee under $30",
    "oversized flannel shirt",
    "leather belt under $15",
    "90s slip dress size M",
    "low-rise cargo pants",
    "mesh long-sleeve top size S/M",
    "crewneck sweatshirt under $25",
    "faded band tee",
    "graphic hoodie size L",
    "suede chelsea boots",
]
SPARE_GOOD = ["velvet blazer", "bucket hat", "denim vest", "henley long sleeve"]

# Criterion 1's three bad queries: malformed JSON, empty query, no-match.
BAD = [
    ("malformed_json", "{not json"),
    ("empty_query", json.dumps({"query": "   "})),
    ("no_match", json.dumps({"query": "ballgown size XXS under $2"})),
]

EMPTY_WARDROBE = [
    "vintage polo shirt",
    "platform sneakers",
    "linen blazer",
    "tie-dye long sleeve",
    "corduroy wide-leg pants",
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def http(method: str, url: str, body: str | None = None, timeout: float = 180) -> dict:
    """One request. Never raises: a failure is a result, and it gets saved."""
    data = body.encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    if body is not None:
        req.add_header("Content-Type", "application/json")
    sent = now()
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status, raw = resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        status, raw = exc.code, exc.read().decode("utf-8", "replace")
    except Exception as exc:  # noqa: BLE001 — timeouts, resets, DNS
        status, raw = None, f"{type(exc).__name__}: {exc}"
    client_ms = round((time.perf_counter() - t0) * 1000)
    try:
        parsed = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        parsed = None
    return {"sent": sent, "client_ms": client_ms, "status": status, "json": parsed,
            "raw": None if parsed is not None else raw}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("trial", type=int)
    ap.add_argument("--base", default=BASE)
    args = ap.parse_args()
    base = args.base.rstrip("/")

    out = ROOT / "results" / "capstone" / f"trial{args.trial}"
    if out.exists() and any(out.iterdir()):
        sys.exit(f"{out} already has results. Trials are never overwritten; pick a new number.")
    out.mkdir(parents=True, exist_ok=True)

    calls: list[dict] = []

    def record(kind: str, criterion: list[int], label: str, method: str, path: str,
               body: str | None = None) -> dict:
        r = http(method, base + path, body)
        entry = {"n": len(calls) + 1, "kind": kind, "criteria": criterion, "label": label,
                 "method": method, "path": path, "body": body, **r}
        calls.append(entry)
        outcome = ""
        if isinstance(r["json"], dict) and path == "/ask":
            outcome = "error=" + str(r["json"].get("error"))[:60] if r["json"].get("error") else "ok"
        print(f"  {entry['n']:>2} {method:<4} {path:<14} {str(r['status']):<4} "
              f"{r['client_ms']:>6}ms  {kind:<15} {label[:38]:<38} {outcome}", flush=True)
        return entry

    def ask(kind, crit, query=None, raw_body=None, wardrobe=None):
        if raw_body is None:
            payload = {"query": query}
            if wardrobe is not None:
                payload["wardrobe"] = wardrobe
            raw_body = json.dumps(payload)
        return record(kind, crit, query if query is not None else raw_body, "POST", "/ask", raw_body)

    def is_ok(entry) -> bool:
        j = entry["json"]
        return entry["status"] == 200 and isinstance(j, dict) and not j.get("error") and bool(j.get("fit_card"))

    started = now()
    print(f"Trial {args.trial} against {base}, started {started}")

    record("warmup", [2], "health", "GET", "/health")

    ok_runs = 0
    # 7 good, each followed by /logs (criterion 3)
    for q in GOOD[:7]:
        e = ask("good", [1, 2, 4] if GOOD.index(q) < 5 else [1, 2], q)
        ok_runs += is_ok(e)
        record("logs_check", [3], f"after {q}", "GET", "/logs?n=20")
    # 3 bad, each followed by /logs
    for kind, body in BAD:
        ask(kind, [1], raw_body=body)
        record("logs_check", [3], f"after {kind}", "GET", "/logs?n=20")
    # 3 more good to make 10 for criterion 2
    for q in GOOD[7:]:
        ok_runs += is_ok(ask("good", [2], q))
    # Replace any non-ok run (criterion 2's rule), from the spares, in order
    for q in SPARE_GOOD:
        if ok_runs >= 10:
            break
        ok_runs += is_ok(ask("spare_good", [2], q))
    # 5 empty-wardrobe queries for criterion 5
    for q in EMPTY_WARDROBE:
        ask("empty_wardrobe", [5], q, wardrobe={"items": []})

    record("snapshot", [1, 2, 3], "end-of-trial", "GET", "/logs?n=200")
    finished = now()

    meta = {"trial": args.trial, "base": base, "started": started, "finished": finished,
            "requests": len(calls), "ok_runs_for_c2": ok_runs}
    (out / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    with (out / "calls.jsonl").open("w", encoding="utf-8") as f:
        for c in calls:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    print(f"\nSaved {len(calls)} calls to {out}")
    print(f"Window for Render's Logs tab: {started}  ->  {finished} (UTC)")
    print(f"Next: copy every `[request]` line from that window into {out / 'render_stdout.txt'}")
    print(f"Then: python capstone_score.py {args.trial}")


if __name__ == "__main__":
    main()
