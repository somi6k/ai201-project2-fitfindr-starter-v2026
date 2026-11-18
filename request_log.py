#!/usr/bin/env python3
"""
Structured request log for serve.py. (Capstone: Shape A)

Each request to /ask appends ONE JSON object, on its own line, to
logs/requests.jsonl. That includes failed requests and rejected ones. The
same line is also printed to stdout, so the host's log viewer shows it even
after the free instance wipes its disk.

    python request_log.py tail [N]     print the last N records (default 10)
    python request_log.py summary      count, outcomes, latency, tokens per run

Fields in every record:
    ts             UTC time the request arrived, ISO 8601
    request_id     short random id, to match the stdout line to the file line
    route          "/ask"
    query          what came in (None if the body had no usable query)
    body_preview   first 200 chars of the raw body, only on bad_request
    status         HTTP status returned
    outcome        ok | no_results | agent_error | exception | bad_request
    error          session["error"] or the exception text; None on success
    tools_run      which steps actually produced output, in order
    n_results      how many listings search_listings returned
    selected_id    id of the listing chosen for the outfit
    fit_card       what came out (the caption), None if the run ended early
    wait_ms        time spent queued behind another request (the lock)
    duration_ms    total time from request arrival to response, including wait
    api_calls      live model API calls this request (retries included; cache hits excluded)
    cache_hits     model answers served from the local cache instead (cost 0)
    prompt_tokens  input tokens the service reported for this request
    output_tokens  output tokens the service reported for this request
"""

import json
import os
import sys
from pathlib import Path

import config

LOG_PATH = Path(os.getenv("AI201_LOG_PATH", config.ROOT / "logs" / "requests.jsonl"))


def write(record: dict) -> None:
    """Append one record. Logging must never break a request, so errors go to stderr."""
    line = json.dumps(record, ensure_ascii=False, default=str)
    print(f"[request] {line}", flush=True)
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError as exc:
        print(f"[request_log] could not write {LOG_PATH}: {exc}", file=sys.stderr, flush=True)


def read_all() -> list[dict]:
    if not LOG_PATH.exists():
        return []
    records = []
    for raw in LOG_PATH.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if raw:
            try:
                records.append(json.loads(raw))
            except json.JSONDecodeError:
                pass
    return records


def _pct(values: list[float], p: float) -> float:
    s = sorted(values)
    k = max(0, min(len(s) - 1, round(p / 100 * (len(s) - 1))))
    return s[k]


def summary(records: list[dict]) -> str:
    if not records:
        return f"No records in {LOG_PATH}"
    out = [f"{len(records)} records in {LOG_PATH}"]
    outcomes: dict[str, int] = {}
    for r in records:
        outcomes[r.get("outcome", "?")] = outcomes.get(r.get("outcome", "?"), 0) + 1
    out.append("outcomes: " + ", ".join(f"{k}={v}" for k, v in sorted(outcomes.items())))

    durations = [r["duration_ms"] for r in records if isinstance(r.get("duration_ms"), (int, float))]
    if durations:
        out.append(
            f"duration_ms: mean={sum(durations) / len(durations):.0f} "
            f"p50={_pct(durations, 50):.0f} p90={_pct(durations, 90):.0f} max={max(durations):.0f}"
        )

    # Cost per run = successful runs that reached the model with no cache help.
    uncached = [r for r in records
                if r.get("outcome") == "ok" and r.get("api_calls") and not r.get("cache_hits")]
    if uncached:
        p = [r.get("prompt_tokens") or 0 for r in uncached]
        o = [r.get("output_tokens") or 0 for r in uncached]
        out.append(
            f"tokens per successful uncached run ({len(uncached)} runs): "
            f"prompt mean={sum(p) / len(p):.0f}, output mean={sum(o) / len(o):.0f}"
        )
    else:
        out.append("tokens: no uncached runs with model calls yet (set AI201_CACHE=0 to measure cost)")
    return "\n".join(out)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "tail"
    recs = read_all()
    if cmd == "tail":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        for r in recs[-n:]:
            print(json.dumps(r, ensure_ascii=False))
    elif cmd == "summary":
        print(summary(recs))
    else:
        print(__doc__)
