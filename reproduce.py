#!/usr/bin/env python3
"""
reproduce.py: Announced vs. Deliverable AI Power Demand (v1)
=============================================================
Measures how much *announced* generation-interconnection capacity in PJM
actually reaches commercial operation ("In Service"), using PJM's own
resolved serial queue. The realized "announced -> deliverable" completion
rate is the deflation factor at the heart of the contingent-vs-deliverable split.

Successor to the bot-energy paper (Zenodo concept DOI 10.5281/zenodo.20512703);
same discipline: a real headline number multiplied against a *contaminated set*
and quoted as if it were firm. Here the contaminated set is the
interconnection queue (projects that mostly withdraw); there it was
bot-vs-human traffic share.

VERSION RECORD (confirmed 2026-08-16)
--------------------------------------
* BUILT = "In Service" ONLY (conservative, matching paper). Under-construction
  MW are treated as reached-IA but unbuilt.
* Re-run confirmed on mature 2010-2017 cohort: 204.4 GW entered -> 46.5 GW
  built = 22.8% realized completion (r2 = 39.1%, r3 = 58.1%).
* "r2 x r3 = 22.8%" is an algebraic identity (built/entered), not an
  independent consistency check.

DATA SOURCE (obtain it yourself: not redistributed here)
---------------------------------------------------------
PJM > Planning > Service Requests > "Serial Service Request Status"
  https://www.pjm.com/planning/service-requests/serial-service-request-status
Use the page's export button to download the project table as XLSX and
save it as the DATA_PATH below. (PJM Data Miner 2 / planning data carry a
redistribution restriction; this script therefore *fetches locally* and
publishes only derived aggregates. NOTE: this means the script is
reproducible only by someone who has obtained PJM access; it is not
turnkey for a reviewer without the file.)
Companion "Cycle Service Request Status" export (CycleProjects-All.xlsx)
is the AI-era cluster cohort, used in the load-side follow-on (not v0).

METHOD (one cohort, one dataset, conditional milestones -> no double-count)
--------------------------------------------------------------------------
1. Filter to Generation Interconnection.
2. Control for cohort maturity: recent projects have not had *time* to
   resolve, which artificially depresses completion. Headline uses a
   mature, (near-)fully-resolved submitted-year window. NOTE: this mature
   cohort is generic historical generation (wind/solar/gas), used as a
   completion BASE RATE; it is not itself "generation announced to serve
   AI." Transfer to the AI cohort is the named load-bearing assumption.
3. Realized completion  = MW reaching "In Service" / MW entered.
4. Decompose into conditional rates (each measured on the prior survivors,
   so multiplying is valid):
       r2 viability = MW reaching an executed Interconnection Agreement / MW entered
       r3 build     = MW In Service / MW reaching an executed IA
   r2 * r3 = built/entered BY DEFINITION (an identity, printed as a
   decomposition; not an independent check).

Every knob below is a defensible analyst choice; change it and watch the
number move. OOM honesty, not false precision.

Author: NM AI Research  ·  ORCID 0009-0003-4213-7769  ·  CC BY 4.0
"""
import os
import sys
import pandas as pd

CANDIDATE_DATA_PATHS = [
    os.path.expanduser("~/Desktop/Reference PDFs/AI_Energy/PlanningQueues.xlsx"),
    os.path.expanduser("~/Desktop/AI_Energy/PlanningQueues.xlsx"),
]
DATA_PATH      = next((p for p in CANDIDATE_DATA_PATHS if os.path.exists(p)), CANDIDATE_DATA_PATHS[0])
SHEET          = "Data"
PROJECT_TYPE   = "Generation Interconnection"
MW_BASIS       = "MW Energy"          # robustness knob: try "MW Capacity"
COHORT_START   = 2010                 # headline mature window (inclusive)
COHORT_END     = 2017
SUBMIT_COL     = "Submitted Date"
STATUS_COL     = "Status"
IA_COL         = ("Interim/Interconnection Service/"
                  "Generation Interconnection Agreement Status")
FEAS_COL       = "Feasibility Study Status"
SIS_COL        = "System Impact Study Status"

# v0.1: BUILT = "In Service" only (conservative, matches the paper). The
# "Partially in Service - Under Construction" status is now treated as
# ADVANCED (reached-IA, not yet built), not as built.
BUILT_STATUSES    = {"In Service"}
ADVANCED_STATUSES = {"Partially in Service - Under Construction",
                     "Under Construction", "Engineering and Procurement"}
# WMPA sensitivity (confirmed 2026-08-16):
# Excluding interim Wholesale Market Participation Agreements (IA_STRICT=1)
# shifts r2 from 39.1% down to 38.0% (r3 from 58.1% up to 59.8%), while
# realized completion is identical at 22.8% (built/entered does not pass IA).
IA_STRICT = os.environ.get("IA_STRICT", "0") == "1"
IA_EXECUTED_VALS = ({"Document Posted"} if IA_STRICT else
                    {"Document Posted", "Wholesale Market Participation Agreement"})
POSTED            = "Document Posted"

# maturation table buckets: (start, end_inclusive, label)
BUCKETS = [(0, 2009, "<=2009"), (2010, 2014, "2010-14"), (2015, 2017, "2015-17"),
           (2018, 2020, "2018-20"), (2021, 2100, "2021-25")]
# ===========================================================================

# Optional CLI override of the basis knob (default stays "MW Energy", the
# headline basis). For the robustness check, run:
#   python3 reproduce_v0.1.py "MW Capacity"
if len(sys.argv) > 1 and sys.argv[1] in ("MW Energy", "MW Capacity"):
    MW_BASIS = sys.argv[1]


def load():
    if not os.path.exists(DATA_PATH):
        sys.exit(
            f"\n  Data file not found: {DATA_PATH}\n"
            "  Download it from PJM 'Serial Service Request Status':\n"
            "    https://www.pjm.com/planning/service-requests/"
            "serial-service-request-status\n"
            "  (use the export button -> XLSX) and save to the path above.\n")
    df = pd.read_excel(DATA_PATH, sheet_name=SHEET, engine="openpyxl")
    df = df[df["Project Type"] == PROJECT_TYPE].copy()
    df["MW"] = pd.to_numeric(df[MW_BASIS], errors="coerce").fillna(0.0)
    df["yr"] = pd.to_datetime(df[SUBMIT_COL], errors="coerce").dt.year
    return df


def maturation_table(df):
    """Completion by submitted cohort -> exposes the cohort-maturity trap."""
    print(f"\n[1] MATURATION: completion by submitted cohort "
          f"({MW_BASIS}-weighted)\n")
    print(f"{'cohort':<10}{'n':>6}{'GW_in':>8}{'%resolved':>11}"
          f"{'%built':>9}{'%withdrawn':>12}")
    for lo, hi, lab in BUCKETS:
        d = df[(df.yr >= lo) & (df.yr <= hi)]
        tot = d.MW.sum()
        if tot == 0:
            continue
        built     = d[d[STATUS_COL].isin(BUILT_STATUSES)].MW.sum()
        withdrawn = d[d[STATUS_COL] == "Withdrawn"].MW.sum()
        terminal  = d[d[STATUS_COL].isin(
            BUILT_STATUSES | {"Withdrawn", "Retracted", "Deactivated",
                              "Annulled", "Canceled"})].MW.sum()
        print(f"{lab:<10}{len(d):>6}{tot/1000:>8.1f}{100*terminal/tot:>11.0f}"
              f"{100*built/tot:>9.1f}{100*withdrawn/tot:>12.0f}")
    print("\n   (recent cohorts read low on %built only because they are not "
          "yet resolved\n    -> headline uses the mature window below.)")
    print("   (%withdrawn = Status=='Withdrawn' only; other exits "
          "(Retracted/Canceled/...) sit in %resolved but not this column.)")


def funnel(df):
    """Conditional funnel on the mature headline cohort."""
    c = df[(df.yr >= COHORT_START) & (df.yr <= COHORT_END)].copy()
    E = c.MW.sum()

    c["built"]   = c[STATUS_COL].isin(BUILT_STATUSES)
    c["adv"]     = c[STATUS_COL].isin(ADVANCED_STATUSES)
    # monotonic: anything built/under-construction necessarily executed an IA
    c["reachIA"]   = (c[IA_COL].isin(IA_EXECUTED_VALS) | c.built | c.adv)
    c["reachSIS"]  = ((c[SIS_COL] == POSTED) | c.reachIA)
    c["reachFeas"] = ((c[FEAS_COL] == POSTED) | c.reachSIS)

    def gw(m):  return c.loc[m, "MW"].sum() / 1000
    def pc(m):  return 100 * c.loc[m, "MW"].sum() / E

    print(f"\n[2] FUNNEL: Generation Interconnection, submitted "
          f"{COHORT_START}-{COHORT_END} ({MW_BASIS}-weighted)\n")
    print(f"   {'stage':<28}{'GW':>8}{'% entered':>11}")
    print(f"   {'Entered queue':<28}{E/1000:>8.1f}{100.0:>11.1f}")
    for lab, m in [("Reached Feasibility", c.reachFeas),
                   ("Reached System Impact", c.reachSIS),
                   ("Reached IA-executed", c.reachIA),
                   ("+ Under construction/E&P", c.built | c.adv),
                   ("BUILT (In Service)", c.built)]:
        print(f"   {lab:<28}{gw(m):>8.1f}{pc(m):>11.1f}")

    r2 = c.loc[c.reachIA, "MW"].sum() / E
    r3 = c.loc[c.built, "MW"].sum() / c.loc[c.reachIA, "MW"].sum()
    print(f"\n   r2 viability (entered -> IA-executed) = {100*r2:5.1f}%")
    print(f"   r3 build     (IA-executed -> service)  = {100*r3:5.1f}%")
    print(f"   r2 x r3 = {100*r2*r3:.1f}%   realized built = {pc(c.built):.1f}%"
          f"   (identity: built/entered, not an independent check)")

    pre  = E - c.loc[c.reachIA, "MW"].sum()
    post = c.loc[c.reachIA, "MW"].sum() - c.loc[c.built | c.adv, "MW"].sum()
    print(f"\n   WHERE THE MW DIE:")
    print(f"     before IA (study / cost-reveal): {pre/1000:6.1f} GW "
          f"= {100*pre/E:.0f}% of entered")
    print(f"     after a signed IA (still unbuilt): {post/1000:6.1f} GW "
          f"= {100*post/E:.0f}% of entered")
    return r2, r3, pc(c.built)


CANDIDATE_CLUSTER_PATHS = [
    os.path.expanduser("~/Desktop/Reference PDFs/AI_Energy/CycleProjects-All.xlsx"),
    os.path.expanduser("~/Desktop/AI_Energy/CycleProjects-All.xlsx"),
]
CLUSTER_PATH = next((p for p in CANDIDATE_CLUSTER_PATHS if os.path.exists(p)), CANDIDATE_CLUSTER_PATHS[0])


def dedup_cluster():
    """r1 de-dup factor on PJM's post-2023 cluster cohort (the factor v0 deferred).

    The cluster export ('Cycle Service Request Status') is the AI-surge vintage.
    It is still Generation Interconnection (supply), not literal data-centre load.
    r1 is bracketed by two keys -> the band, not a point, is the result.
    """
    if not os.path.exists(CLUSTER_PATH):
        print(f"\n[skip cluster/r1] file not found: {CLUSTER_PATH}\n"
              "  Download PJM 'Cycle Service Request Status' -> XLSX to that path.")
        return
    df = pd.read_excel(CLUSTER_PATH, sheet_name="Data", engine="openpyxl")
    g = df[df["Project Type"] == PROJECT_TYPE].copy()
    g["MW"] = pd.to_numeric(g["MW Energy"], errors="coerce").fillna(0.0)
    g = g[g["MW"] > 0].copy()                 # real generation only
    filed = g["MW"].sum()

    g["mwr"] = g["MW"].round(0)
    strict_keys = ["Developer", "State", "County", "Fuel", "mwr"]
    loose_keys  = ["Developer", "State", "County"]
    # collapse each cluster to its single largest filing
    uniq_strict = (g.sort_values("MW", ascending=False)
                     .drop_duplicates(subset=strict_keys)["MW"].sum())
    uniq_loose  = (g.sort_values("MW", ascending=False)
                     .drop_duplicates(subset=loose_keys)["MW"].sum())
    r1_strict, r1_loose = uniq_strict / filed, uniq_loose / filed
    withdrawn = g[g["Status"] == "Withdrawn"]["MW"].sum()
    built = pd.to_numeric(g["MW In Service"], errors="coerce").fillna(0).sum()

    print("\n[3] LOAD-SIDE EXTENSION: r1 de-duplication on the AI-era cluster "
          "cohort\n    (TC1/TC2/C01; Generation Interconnection; MW-Energy)\n")
    print(f"    non-zero-MW projects: {len(g)}   filed: {filed/1000:.0f} GW")
    print(f"    r1 strict (Dev+State+County+Fuel+MW): {r1_strict:.3f}  "
          f"(removes {100*(1-r1_strict):.1f}% as literal duplicate)")
    print(f"    r1 loose  (Dev+State+County):         {r1_loose:.3f}  "
          f"(removes {100*(1-r1_loose):.1f}%)")
    print(f"    => r1 band = {r1_loose:.2f}-{r1_strict:.2f}")
    print(f"    NOTE: this measures LITERAL DUPLICATES only (~8-19%). The "
          "'5-10x phantom'\n    prior, read broadly as 'MW that never get "
          "built', is NOT refuted: the\n    realized completion above already "
          "implies ~5x non-completion. The narrow\n    finding is only that the "
          "inflation is viability/withdrawal-driven, not\n    duplicate-driven.")
    print(f"    already withdrawn: {100*withdrawn/filed:.0f}% of MW   "
          f"built (In Service): {built/1000:.1f} GW (cohort too young -> "
          f"r3 stays from serial)")


def main():
    print("=" * 64)
    print("Announced vs. Deliverable AI Power Demand: v1 (PJM serial queue)")
    print(f"basis: {MW_BASIS}  |  source: {os.path.basename(DATA_PATH)}")
    print("=" * 64)
    df = load()
    print(f"\nGeneration Interconnection projects: {len(df)}  |  "
          f"total announced: {df.MW.sum()/1000:.0f} GW ({MW_BASIS})")
    maturation_table(df)
    funnel(df)
    dedup_cluster()
    print("\n[note] generation SUPPLY contingency, not the ~950 TWh demand "
          "figure;\n       'built' = In Service ONLY (under-construction "
          "excluded, conservative);\n       mature cohort = generic historical "
          "generation used as a BASE RATE;\n       serial = pre-2023 process; "
          "cluster = AI-era (FERC Order 2023);\n       cohort comparability is "
          "the load-bearing assumption.\n")


if __name__ == "__main__":
    main()
