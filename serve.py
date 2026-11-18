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

Capstone instrumentation: every /ask request, including a rejected or failed
one, writes one JSON record to logs/requests.jsonl (and to stdout) through
request_log.py. It records timing, outcome, tools run, and per-request token
counts. `python request_log.py summary` reads the log back.
"""

import os
import sys
import threading
import time
import uuid
from datetime import datetime, timezone

# config first, and before anything that talks to the model: it loads your .env
# and fixes the Windows console encoding for every module that imports it.
import config  # noqa: F401

from flask import Flask, jsonify, request

import generate
import request_log
from agent import run_agent
from utils.data_loader import get_example_wardrobe

app = Flask(__name__)


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
    record = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
        "request_id": uuid.uuid4().hex[:8],
        "route": "/ask",
        "query": None,
    }

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        payload = {}
    raw_query = payload.get("query")
    query = raw_query.strip() if isinstance(raw_query, str) else ""
    if not query:
        # 400 rather than a stack trace: the caller can act on this one.
        message = ("Send JSON with a 'query' field, e.g. "
                   '{"query": "vintage graphic tee under $30"}')
        record["body_preview"] = request.get_data(as_text=True)[:200]
        record.update(_empty_run_fields())
        record.update(status=400, outcome="bad_request", error=message,
                      duration_ms=_ms_since(started))
        request_log.write(record)
        return jsonify({"error": message}), 400
    record["query"] = query

    wardrobe = payload.get("wardrobe")
    if not isinstance(wardrobe, dict):
        wardrobe = get_example_wardrobe()

    # A queued request should look like a queued request. Without this the
    # second caller just sits there, and "slow" and "waiting its turn" are
    # indistinguishable from the outside — which is how people conclude the
    # deployment is broken when it is behaving exactly as designed.
    #
    # This is NOT the logging you add in the follow-along. It prints nothing
    # on the normal path, carries no timing and counts nothing; it says only
    # that this request had to wait. `locked()` can be a moment out of date,
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
    with _one_at_a_time:
        # Inside the lock, so the before/after token snapshot covers this
        # request only. generate.py's counters are process-wide running totals.
        wait_ms = _ms_since(started)
        before = _usage_snapshot()
        try:
            session = run_agent(query, wardrobe)
        except Exception as exc:  # noqa: BLE001 — a 500 with a sentence beats a hang
            failure = f"{type(exc).__name__}: {exc}"
        after = _usage_snapshot()

    # Outside the lock: building a response is not work the next caller should
    # be waiting on.
    record.update(_run_fields(session))
    record["wait_ms"] = wait_ms
    record.update({k: after[k] - before[k] for k in before})
    if failure is not None:
        record.update(status=500, outcome="exception", error=failure)
    elif session.get("error"):
        # The agent stopped early on purpose (e.g. nothing matched). Still a 200.
        outcome = "no_results" if not session.get("search_results") else "agent_error"
        record.update(status=200, outcome=outcome, error=session["error"])
    else:
        record.update(status=200, outcome="ok", error=None)
    record["duration_ms"] = _ms_since(started)
    request_log.write(record)

    if failure is not None:
        return jsonify({"error": failure}), 500

    return jsonify(session)


# ── instrumentation helpers ───────────────────────────────────────────────────

def _ms_since(t0: float) -> int:
    return round((time.perf_counter() - t0) * 1000)


def _usage_snapshot() -> dict:
    tokens = generate.token_counts()
    return {
        "api_calls": generate.call_count(),
        "cache_hits": generate._cache_hits,
        "prompt_tokens": tokens["prompt"],
        "output_tokens": tokens["output"],
    }


def _empty_run_fields() -> dict:
    return {"tools_run": [], "n_results": None, "selected_id": None, "fit_card": None,
            "wait_ms": 0, "api_calls": 0, "cache_hits": 0,
            "prompt_tokens": 0, "output_tokens": 0}


def _run_fields(session: dict | None) -> dict:
    """What the agent got through, read from the session it returned."""
    if not session:
        return {"tools_run": [], "n_results": None, "selected_id": None, "fit_card": None}
    tools = []
    if session.get("parsed"):
        tools.append("parse_query")
    if session.get("selected_item") is not None or session.get("error"):
        tools.append("search_listings")
    if session.get("outfit_suggestion"):
        tools.append("suggest_outfit")
    if session.get("fit_card"):
        tools.append("create_fit_card")
    item = session.get("selected_item") or {}
    return {
        "tools_run": tools,
        "n_results": len(session.get("search_results") or []),
        "selected_id": item.get("id"),
        "fit_card": session.get("fit_card"),
    }


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
