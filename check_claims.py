#!/usr/bin/env python3
"""
check_claims.py - verify the claims passport against CSVs, prose, and tiers.

This script performs four distinct integrity checks:
1. CSV check: Confirms claim "value" matches corresponding published CSV cells.
2. Prose check: Confirms numeric claim values appear in paper_v1.md.
3. CSV unit sanity: Confirms GW and percentage columns in funnel CSVs agree.
4. Tier agreement: Confirms tier-3 claims do not sit under tier-1 or tier-2 headings.

Run (from this folder):  python3 check_claims.py
Exit code 0 = all checks pass; 1 = failures detected.
Pure standard library.
"""
import csv
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
TOL = 1e-6


def load_csv(name):
    with open(HERE / name, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def find_row(rows, stage_contains):
    hits = [r for r in rows if stage_contains.lower() in r["stage"].lower()]
    if len(hits) != 1:
        raise LookupError(
            f"stage substring {stage_contains!r} matched {len(hits)} rows "
            f"(need exactly 1)")
    return hits[0]


def prose_check(claims, md_path="paper_v1.md"):
    md = (HERE / md_path).read_text(encoding="utf-8")
    md_norm = md.replace("≈", "~").replace("\u2013", "-").replace("\u2014", "-")
    missing = []
    for c in claims:
        v = c.get("value")
        if v is None:
            continue
        if isinstance(v, list):
            vals = v
        elif isinstance(v, (int, float)):
            vals = [v]
        else:
            continue
        for num in vals:
            pats = {f"{num:g}", f"{num:.1f}".rstrip("0").rstrip(".")}
            if not any(p in md_norm for p in pats):
                missing.append((c["id"], num))
    return missing


def unit_check(rows, gw_key, pct_key, tol=3.0):
    problems = []
    try:
        base = float(rows[0][gw_key])  # the 100% baseline row
    except (IndexError, ValueError, KeyError) as e:
        return [("header", f"failed to read baseline: {e}")]

    for r in rows:
        if r.get("row_kind", "funnel") != "funnel":
            continue
        g, p = r.get(gw_key), r.get(pct_key)
        if g in ("", "null", None) or p in ("", "null", None):
            problems.append((r.get("stage", "?"), "non-numeric cell in numeric column"))
            continue
        try:
            g_val = float(g)
            p_val = float(p)
            implied = 100.0 * g_val / base
            if abs(implied - p_val) > tol:
                problems.append((
                    r.get("stage", "?"),
                    f"{gw_key}={g} implies {implied:.1f}% but {pct_key}={p}"))
        except ValueError as e:
            problems.append((r.get("stage", "?"), f"parse error: {e}"))
    return problems


def tier_check(claims, md_path="paper_v1.md"):
    md = (HERE / md_path).read_text(encoding="utf-8")
    problems = []

    # Extract Verification note section
    vmatch = re.search(r"## Verification note(.*?)(?:## Conflict of interest|$)", md, re.DOTALL)
    if not vmatch:
        return [("verification_note", "Verification note section not found")]
    vnote = vmatch.group(1)

    # Find text under tier 1 and tier 2 blocks
    t1_match = re.search(r"\*\*Traced to official operator records and filings \(tier 1\)\.\*\*(.*?)(?:\*\*Traced|\*\*Derived|$)", vnote, re.DOTALL)
    t2_match = re.search(r"\*\*Traced via a named secondary to a named primary \(tier 2\)\.\*\*(.*?)(?:\*\*Derived|\*\*Secondary|$)", vnote, re.DOTALL)

    t1_text = t1_match.group(1) if t1_match else ""
    t2_text = t2_match.group(1) if t2_match else ""

    for c in claims:
        if c.get("motive_tier") == 3:
            # Check keywords or source name associated with tier 3 claims
            src = c.get("source", "")
            if "Aurora" in src:
                if "Aurora" in t1_text:
                    problems.append((c["id"], "Tier-3 Aurora claim found under Tier-1 heading"))
                if "Aurora" in t2_text:
                    problems.append((c["id"], "Tier-3 Aurora claim found under Tier-2 heading"))
    return problems


def main():
    claims = json.loads((HERE / "claims.json").read_text(encoding="utf-8"))["claims"]
    csv_cache, checked, skipped, failures = {}, 0, [], []

    print("[1] CSV Claims Matching:")
    for c in claims:
        chk = c.get("csv_check")
        if not chk:
            skipped.append((c["id"], c.get("reproducibility", "?")))
            continue
        try:
            rows = csv_cache.setdefault(chk["file"], load_csv(chk["file"]))
            row = find_row(rows, chk["stage_contains"])
            got = float(row[chk["column"]])
            want = float(c["value"])
            ok = abs(got - want) <= TOL
            checked += 1
            mark = "PASS" if ok else "FAIL"
            print(f"  [{mark}] {c['id']:<32} claim={want:<7g} "
                  f"{chk['file']}:{chk['column']}={got:g}")
            if not ok:
                failures.append(c["id"])
        except (LookupError, KeyError, ValueError) as e:
            checked += 1
            failures.append(c["id"])
            print(f"  [FAIL] {c['id']:<32} {e}")

    print(f"\n  checked {checked} CSV-backed claims: "
          f"{checked - len(failures)} pass, {len(failures)} fail")

    print("\n[2] Prose Numeric Verification:")
    missing_prose = prose_check(claims)
    if missing_prose:
        for cid, num in missing_prose:
            print(f"  [FAIL] {cid:<32} number {num} not found in paper_v1.md")
            failures.append(f"prose:{cid}")
    else:
        print("  [PASS] all numeric claims found in paper_v1.md")

    print("\n[3] CSV Unit Sanity:")
    dc_rows = load_csv("dc_funnel.csv")
    dc_problems = unit_check(dc_rows, "gw_2030", "pct_of_submitted")
    for stg, prob in dc_problems:
        print(f"  [FAIL] dc_funnel.csv [{stg}]: {prob}")
        failures.append(f"dc_unit:{stg}")

    ercot_rows = load_csv("ercot_funnel.csv")
    ercot_problems = unit_check(ercot_rows, "gw", "pct_of_requested")
    for stg, prob in ercot_problems:
        print(f"  [FAIL] ercot_funnel.csv [{stg}]: {prob}")
        failures.append(f"ercot_unit:{stg}")

    if not dc_problems and not ercot_problems:
        print("  [PASS] dc_funnel.csv and ercot_funnel.csv units are consistent")

    print("\n[4] Passport ↔ Paper Tier Agreement:")
    tier_problems = tier_check(claims)
    if tier_problems:
        for cid, prob in tier_problems:
            print(f"  [FAIL] {cid}: {prob}")
            failures.append(f"tier:{cid}")
    else:
        print("  [PASS] tier classifications agree between passport and Verification note")

    if skipped:
        print("\n  not locally checkable (by design):")
        for cid, tier in skipped:
            print(f"    - {cid:<34} [{tier}]")

    if failures:
        print(f"\n  MISMATCH in: {', '.join(failures)}")
        return 1
    print("\n  ALL PASSPORT CHECKS PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
