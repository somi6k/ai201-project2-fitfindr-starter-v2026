#!/usr/bin/env python3
"""
Grade one capstone trial against criteria.md. (Milestone 5)

    python capstone_score.py 1          # reads results/capstone/trial1/, writes score.md there

Inputs, all in results/capstone/trialN/:
    calls.jsonl          raw requests and responses, from capstone_trial.py
    render_stdout.txt    every `[request] {...}` line from Render's Logs tab, pasted in.
                         Copy from the service's most recent start (deploy or wake-up)
                         through the end of the trial, so criterion 3 can line up all 20
                         records. Other lines in the paste are ignored.

Scoring follows criteria.md exactly. The one judgement a script can't make, whether
the item title is "named recognisably" in criterion 4, is pre-checked by word
overlap and printed for a person to confirm. See the TITLE CHECK lines in score.md.
"""

import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).parent
SLACK = timedelta(seconds=5)   # client and server clocks, plus network time


def ts(s: str) -> datetime:
    return datetime.fromisoformat(s)


def load(trial: int):
    d = ROOT / "results" / "capstone" / f"trial{trial}"
    calls = [json.loads(l) for l in (d / "calls.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    stdout_path = d / "render_stdout.txt"
    stdout = None
    if stdout_path.exists():
        stdout = []
        for line in stdout_path.read_text(encoding="utf-8").splitlines():
            i = line.find("[request] {")
            if i >= 0:
                try:
                    stdout.append(json.loads(line[i + len("[request] "):]))
                except json.JSONDecodeError:
                    pass
    return d, calls, stdout


def matches(call: dict, rec: dict) -> bool:
    """Is this log record the one this /ask call produced?"""
    body = call["body"]
    try:
        q = json.loads(body).get("query")
    except (json.JSONDecodeError, AttributeError):
        q = None
    same_input = (rec.get("query") == q.strip()) if isinstance(q, str) and q.strip() \
        else (rec.get("body_preview") == body[:200])
    if not same_input:
        return False
    sent = ts(call["sent"])
    return sent - SLACK <= ts(rec["ts"]) <= sent + timedelta(milliseconds=call["client_ms"]) + SLACK


def find(call, records):
    for r in records or []:
        if matches(call, r):
            return r
    return None


# ── criterion 4 helpers ───────────────────────────────────────────────────────

_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen " \
        "fifteen sixteen seventeen eighteen nineteen".split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def spelled(n: int) -> list[str]:
    if n < 20:
        return [_ONES[n]]
    t, o = divmod(n, 10)
    return [_TENS[t]] if o == 0 else [f"{_TENS[t]}-{_ONES[o]}", f"{_TENS[t]} {_ONES[o]}"]


def has_price(card: str, price: float) -> bool:
    n = int(price)
    low = card.lower()
    if re.search(rf"\${n}(\.00)?\b", card) or re.search(rf"\b{n}(\.00)?\s*(bucks|dollars)\b", low):
        return True
    return any(w in low for w in spelled(n))


def has_platform(card: str, platform: str) -> bool:
    norm = lambda s: re.sub(r"[^a-z]", "", s.lower())
    return norm(platform) in norm(card)


STOP = {"the", "a", "and", "of", "vintage", "90s", "y2k", "style", "with"}


def title_overlap(card: str, title: str) -> list[str]:
    # Whole title, including the descriptor after the dash ("Floral, Midi Length").
    words = [w for w in re.findall(r"[a-z]+", title.lower()) if w not in STOP and len(w) > 2]
    low = card.lower()
    return [w for w in words if w in low]


def sentences(text: str) -> int:
    parts = re.split(r"(?<=[.!?])\s+|\n+", text or "")
    return sum(1 for p in parts if len(re.findall(r"[A-Za-z]+", p)) >= 3)


# ── scoring ───────────────────────────────────────────────────────────────────

def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    trial = int(sys.argv[1])
    d, calls, stdout = load(trial)
    snapshot = next(c for c in calls if c["kind"] == "snapshot")
    snap_records = (snapshot["json"] or {}).get("records", [])
    asks = [c for c in calls if c["path"] == "/ask"]
    lines = [f"# Capstone trial {trial}: score", ""]
    rows = {}

    # Criterion 1: 7 good + 3 bad, each has a [request] line in Render's stdout
    c1 = [c for c in asks if 1 in c["criteria"]]
    lines.append("## Criterion 1: every query leaves a `[request]` line in Render's log output")
    if stdout is None:
        rows[1] = "needs render_stdout.txt"
        lines.append("Not scored: render_stdout.txt is missing.")
    else:
        hits = 0
        for c in c1:
            r = find(c, stdout)
            hits += r is not None
            lines.append(f"- {'PASS' if r else 'FAIL'} {c['kind']:<15} {c['label'][:40]!r:<44} "
                         f"-> {('request_id ' + r['request_id'] + ', outcome ' + r['outcome']) if r else 'no matching line'}")
        rows[1] = f"{hits}/{len(c1)}"
    lines.append("")

    # Criterion 2: first 10 `ok` runs, server duration_ms <= 10000
    lines.append("## Criterion 2: 9 of 10 warm `ok` runs finish within 10 s (server `duration_ms`)")
    warm = next(c for c in calls if c["kind"] == "warmup")
    lines.append(f"Warm-up: GET /health -> {warm['status']} in {warm['client_ms']} ms (client)")
    ok_calls = [c for c in asks if c["kind"] in ("good", "spare_good")
                and c["status"] == 200 and isinstance(c["json"], dict)
                and not c["json"].get("error") and c["json"].get("fit_card")]
    replaced = [c for c in asks if c["kind"] in ("good", "spare_good") and c not in ok_calls]
    for c in replaced:
        lines.append(f"- replaced (not ok): {c['label']!r} status={c['status']} "
                     f"error={str((c['json'] or {}).get('error') or c.get('raw'))[:100]!r}")
    under = 0
    durations = []
    for c in ok_calls[:10]:
        r = find(c, snap_records) or find(c, stdout)
        dur = r["duration_ms"] if r else None
        durations.append(dur)
        ok = dur is not None and dur <= 10000
        under += ok
        lines.append(f"- {'PASS' if ok else 'FAIL'} {c['label']!r:<36} duration_ms={dur}  (client {c['client_ms']} ms)")
    if len(ok_calls) < 10:
        lines.append(f"Only {len(ok_calls)} ok runs; spares ran out.")
    rows[2] = f"{under}/{min(10, len(ok_calls))}"
    lines.append("")

    # Criterion 3: each /logs call returns the latest min(20, on-disk) records, matching stdout
    lines.append("## Criterion 3: /logs returns the latest 20 entries (or all, if fewer), matching Render's stdout")
    checks = [c for c in calls if c["kind"] == "logs_check"]
    if stdout is None:
        rows[3] = "needs render_stdout.txt"
        lines.append("Not scored: render_stdout.txt is missing.")
    else:
        ids = [r["request_id"] for r in stdout]
        first_ts = ts(stdout[0]["ts"]) if stdout else None
        good3 = 0
        for c in checks:
            prev = calls[c["n"] - 2]          # the /ask just before this /logs call
            j = c["json"] or {}
            R = j.get("records") or []
            reasons, notes = [], []
            if c["status"] != 200:
                reasons.append(f"status {c['status']}")
            if len(R) != min(20, j.get("count_on_disk", -1)):
                reasons.append(f"{len(R)} records but count_on_disk={j.get('count_on_disk')}")
            # What the criterion says: the latest entries, as compared against Render's stdout.
            # Expected = stdout up to the newest record from any /ask sent before this call.
            # Anchored on request order, not clocks: Render's clock and mine differ by more
            # than a 0 ms bad request takes, so a timestamp cut-off misplaces those records.
            k = -1
            for a in calls[: c["n"] - 1]:
                if a["path"] == "/ask":
                    r = find(a, stdout)
                    if r is not None:
                        k = max(k, ids.index(r["request_id"]))
            before = ids[: k + 1]
            got = [r["request_id"] for r in R]
            # Records older than the first pasted line can't be checked, so they are allowed.
            older = [r for r in R if first_ts and ts(r["ts"]) < first_ts]
            checkable = got[len(older):]
            mismatch = (checkable != before[-len(checkable):]) if checkable else bool(before)
            if mismatch:
                reasons.append(f"returned {got[-3:]}… but stdout's latest are {before[-3:]}…")
            # Not part of criterion 3 (it's criterion 1's job), but worth seeing:
            if R and not matches(prev, R[-1]):
                notes.append("note: the request just sent has no record in /logs OR stdout")
            ok = not reasons
            good3 += ok
            lines.append(f"- {'PASS' if ok else 'FAIL'} {c['label']:<40} {len(R)} records"
                         f"{'' if ok else '  (' + '; '.join(reasons) + ')'}"
                         f"{'  [' + '; '.join(notes) + ']' if notes else ''}")
        rows[3] = f"{good3}/{len(checks)}"
    lines.append("")

    # Criterion 4: fit card names title, price, platform. 5 different queries
    lines.append("## Criterion 4: fit card names the item's title, price and platform")
    c4 = [c for c in asks if 4 in c["criteria"]]
    p4 = 0
    for c in c4:
        j = c["json"] or {}
        item = j.get("selected_item") or {}
        card = j.get("fit_card") or ""
        if not card:
            lines.append(f"- FAIL {c['label']!r}: no fit card (status {c['status']}, error {j.get('error')!r})")
            continue
        price_ok = has_price(card, item["price"])
        plat_ok = has_platform(card, item["platform"])
        overlap = title_overlap(card, item["title"])
        title_ok = bool(overlap)
        ok = price_ok and plat_ok and title_ok
        p4 += ok
        lines.append(f"- {'PASS' if ok else 'FAIL'} {c['label']!r} -> {item['id']} {item['title']!r} "
                     f"${item['price']:.0f} {item['platform']}")
        lines.append(f"    price={'Y' if price_ok else 'N'} platform={'Y' if plat_ok else 'N'} "
                     f"TITLE CHECK (confirm by eye): words matched {overlap or 'none'}")
        lines.append(f"    card: {card}")
    rows[4] = f"{p4}/{len(c4)}"
    lines.append("")

    # Criterion 5: empty wardrobe -> general advice of at least 2 sentences
    lines.append("## Criterion 5: empty wardrobe gets general advice of at least 2 sentences")
    c5 = [c for c in asks if c["kind"] == "empty_wardrobe"]
    p5 = 0
    for c in c5:
        j = c["json"] or {}
        adv = j.get("outfit_suggestion") or ""
        n = sentences(adv)
        wardrobe_sent = (j.get("wardrobe") or {}).get("items")
        ok = c["status"] == 200 and not j.get("error") and n >= 2 and wardrobe_sent == []
        p5 += ok
        lines.append(f"- {'PASS' if ok else 'FAIL'} {c['label']!r}: {n} sentences, status {c['status']}, "
                     f"wardrobe items on server={wardrobe_sent!r}, error={j.get('error')!r}")
        lines.append(f"    advice: {adv[:400]!r}")
    rows[5] = f"{p5}/{len(c5)}"
    lines.append("")

    head = ["## Summary", "", "| Criterion | Target | Result |", "|---|---|---|",
            f"| 1. Every query logged in Render's output | 10 of 10 | {rows[1]} |",
            f"| 2. Warm ok runs within 10 s | 9 of 10 | {rows[2]} |",
            f"| 3. /logs returns latest 20, matching stdout | 10 of 10 | {rows[3]} |",
            f"| 4. Fit card names title, price, platform | 5 of 5 | {rows[4]} |",
            f"| 5. Empty wardrobe gets 2+ sentences of advice | 5 of 5 | {rows[5]} |", ""]
    text = "\n".join(lines[:2] + head + lines[2:])
    (d / "score.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
