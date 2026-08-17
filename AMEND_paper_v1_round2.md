# Amendment note #2 — *Announced vs. Deliverable AI Power Demand* (v1)

**To:** implementing agent
**From:** red-team pass #2, 2026-08-16 (revised after source verification and author direction)
**Supersedes:** `AMEND_paper_v1.md` (round 1), and any earlier copy of this file
**Source of record:** `paper_v1.md` as of 13:05, 2026-08-16 (line numbers refer to that file)
**Artifact state at review:** `paper_v1.pdf`, `paper_v1.html` (13:05) and `index.html` (13:01) are current with the CSVs and markdown. `check_claims.py` passes 7/7 — while three of the bugs below are live, which is the point of **R13**.

---

## §0 — Rules of engagement

1. **Do not invent a reconciliation. Escalate instead.** Three items (**R2**, **R7**, **R8**) are settled by documents that are **on this machine** — paths given inline. Open them and resolve from source. If a document does not actually state the answer, **stop that item and report back to Noel**. Do not substitute a plausible mechanism. The paper's own COI section names this failure mode: prose that "is locally plausible and consistent in tone with what surrounds it."
2. **Author decisions already taken** (do not re-open):
   - **R1** — the cross-region finding leads with the *empirical* axis only. Rationale and full text in R1.
   - **R11** — "Google Gemini 3.7" is confirmed correct. **Struck. No action.**
   - **R12** — the DOIs are correct as they stand. **Struck. No action.** See the verification record below so this is not re-litigated.
3. **Do not re-break round 1.** §1 lists what round 1 fixed correctly. Before overwriting any line that records *why* a value is what it is, preserve that record.
4. **Propagation rule.** Any changed figure lands in **all** of: `paper_v1.md` → `claims.json` → the relevant CSV → `python3 build.py` (regenerates `index.html`) → regenerate `paper_v1.html` / `paper_v1.pdf`.
5. `python3 check_claims.py` must exit 0 at the end, **with R13's new checks active**.
6. **`build.py` does not build the paper.** It only re-embeds CSVs into `index.html`. Use whatever pipeline produced the 13:05 artifacts (Chrome headless print); verify after with `pdfinfo paper_v1.pdf` that the title reads *Announced vs. Deliverable AI Power Demand (v1)*.
7. **Do not mint a DOI** until §5 is green and Noel has answered the record-id question in `zenodo_paper_v1.json:3`.

### Verification record — DOIs (R12 struck)

Round 1 was suspected of a DOI regression. It was not. Checked against the Zenodo API on 2026-08-16:

| id | resolves as | status |
|---|---|---|
| `20512703` | **concept** DOI of the bot-energy paper (`conceptrecid` of 20562696) | ✅ correctly cited at `paper_v1.md:163` as "concept DOI" |
| `20562696` | bot-energy **v1** (version DOI) | fine; a version DOI, less appropriate for a methods-precedent citation |
| `20512704` | bot-energy **v0** (version DOI) | historical, correctly superseded |
| `20559430` | **concept** DOI of the Contingent series (`conceptrecid` of 20706509) | ✅ correctly cited in `README.md`, `.zenodo.json`, `paper_v1.md:202` |
| `20706509` | Contingent **v0.1** (version DOI) | ✅ correctly cited at `paper_v1.md:202` |

Concept DOIs do not return from `/api/records/<id>`, which is why they read as "not found" on a naive check. Round 1's change from a version DOI to a concept DOI was an improvement — a concept DOI always resolves to the latest version. The only residue is `zenodo_paper_v2.json:38`, which still references the version DOI `20562696`; that file belongs to a retired draft (see **R14**) and needs no edit unless it is being reused.

---

## §1 — Round-1 ledger (do not redo, do not revert)

**Landed correctly — leave alone:** A2 (§9 "separate queues" phrasing), A3 (tier-2 provenance bucket, reworded Guarantee, "motive-neutral" → "independent"), A7 (strawman named in §1 — but see **R6**), A8 (28/26/16pp — but see **R9**), A10 (de-dup key relabelled 7.9% / 19.4%), B1 ("a further 13%" + 3.2pp under construction), B2 (double-70% collapsed), B3 (r2 → 39.1%), B4 (`reproduce.py` stale blocker → VERSION RECORD), C1 (%withdrawn footnote), C3 (§9 non-sequitur deleted), C5 (v0.1 record DOI), A6 (950 TWh / $850B cited — see **R10**).

**A1 landed in substance but was mislabelled** → superseded by **R1**, which changes the framing on author direction.

**Not done, carried forward:** A5 (rail denominators → **R7**), A9 (WMPA magnitude → **R8**), B7 (`check_claims.py` → **R13**), B6 (v2-PDF relationship → **R14**).

**New damage introduced in round 1:** **R5** (`ercot_funnel.csv` unit bug, live on the published site), **R6** ("in private").

**Struck, no action:** R11, R12.

---

## §2 — The fixes

### R1 — Re-pitch the cross-region finding to the empirical axis only  ★ author-directed

**Why.** Round 1 reframed §8 as a two-axis "empirical divergence." Row 2 (70% assumed vs 49.8% metered) is a genuine measurement-vs-assumption comparison. Row 1 (63% accepted vs 15% credible) is not: ERCOT's 15% is Aurora Energy Research's *commissioned forward model* — `ercot_funnel.csv` says so ("Commissioned consulting study for ERCOT board planning", `motive_tier 3`), as does `claims.json:179`. It is model-vs-model.

**Author's decision: lead with the empirical axis only.** The 49.8%-vs-70% comparison becomes the finding. The 15% is demoted to context inside the existing three-quantity split and is **not** presented as a cross-region axis and **not** used in the §9 bracket. This is the strongest claim per unit of evidence.

**(a)** Replace everything from `:130` through `:137` (the "cross-region finding" heading, its table, and the paragraph after it) with:

> **The cross-region finding: metered utilization falls below assumed utilization.** Only one quantity is expressed in comparable terms by both operators, and on that quantity ERCOT's measured outcome is materially worse than PJM's planning assumption.
>
> | Axis | PJM | ERCOT | Basis |
> |---|---|---|---|
> | Post-build peak utilization | 70% | 49.8% | PJM: assumed capacity-to-demand factor applied forward. ERCOT: metered per-site peak ÷ requested MW, non-crypto data centres in service 2022–2024. |
>
> PJM assumes a built data centre draws 70% of its requested capacity at peak. ERCOT measures 49.8% across the sites that have actually been built. That is a ≈1.4× gap on the one figure both operators state the same way, and it points where everything else in this note points: the request over-states the load, and it does so even after the project is built and running.
>
> The forward axis is deliberately not offered as a second comparison. PJM's ≈63% acceptance is an administrative vetting outcome; ERCOT's ≈15% (≈35 GW of ≈226 GW) is a commissioned scenario model. Both are planning judgements rather than measurements, and the ≈4× gap between them reflects two different modelling exercises applied to two differently-padded queues, not evidence that either is correct. ERCOT's scenario is reported in the three-quantity split above as an indication of how padded its queue is, and it does not enter the §9 bracket.
>
> Both operators now gate their planning forecasts on executed agreements.

**(b)** Abstract `:13` — replace:

> empirical data undercuts PJM's forward planning assumptions on both comparable axes: ERCOT's commissioned credible 2030 scenario accepts only ≈15% of requested load (≈35 GW of ≈226 GW), and its metered operational data shows a realized per-site peak consumption of 49.8% of requested MW for completed sites.

with:

> the one quantity both operators state in comparable terms is measured rather than assumed, and it undercuts PJM: ERCOT's metered per-site peak consumption is 49.8% of requested MW across non-crypto data centres built 2022–2024, against the 70% capacity-to-demand factor PJM applies forward. ERCOT's commissioned 2030 scenario is lower again in relative terms (≈35 GW against a ≈226 GW queue), but it is a model rather than a measurement and is reported as context on queue padding, not as a second cross-region axis.

**(c)** `:112` — the §8 lead-in currently promises two things ERCOT publishes. Replace:

> Second, ERCOT publishes both a forward credible scenario and an empirical *realized* post-build de-rate (observed peak against requested MW).

with:

> Second, and uniquely, ERCOT publishes an empirical *realized* post-build de-rate: observed peak consumption against requested MW, for sites that have actually been built. That is the only figure in either region that measures rather than assumes.

**(d)** `:124` — the "Request survival" bullet already states the 15%. Append to it, so the demotion is explicit where a reader meets the number:

> This is a commissioned forward model (Aurora), not an ERCOT measurement, and it is reported here as an indication of how padded the queue is rather than as a cross-region comparison against PJM's ≈63% acceptance, which is itself a planning judgement.

**(e)** `:143` — the §9 upper-rail bullet currently reads "ERCOT's empirical data sits below this rail on both axes (≈15% request survival, 49.8% realized peak)." Replace that sentence with:

> ERCOT contributes no figure to this rail: its ≈15% scenario is a commissioned model, and its 49.8% metered peak measures utilization after build rather than survival into a forecast. Both sit outside the bracket by construction.

**(f)** Restore Aurora to tier 3. Delete from the Verification note's **tier 2** bucket at `:174`:

> The 35 GW credible 2030 scenario from Aurora Energy Research (*ERCOT Resource Adequacy Study*, via Utility Dive).

and add under **Secondary research and market benchmarks (tier 3)** at `:181`:

> - The 35 GW credible 2030 ERCOT data-centre scenario from Aurora Energy Research (*ERCOT Resource Adequacy Study*, commissioned by ERCOT, via Utility Dive). A commissioned forward model, not an operator measurement.

This also repairs a passport disagreement: `claims.json:179` has `motive_tier: 3` while the paper had promoted it to tier 2, and `claims.json:2` states that any such disagreement is "a bug, not a choice."

**(g)** Replace the whole `cross_region` block in `claims.json` (`:195-201`) with:

```json
  "cross_region": {
    "statement": "On the one axis where PJM and ERCOT are comparable like-for-like, ERCOT's metered post-build utilization (49.8%) falls well below PJM's assumed capacity-to-demand factor (70%).",
    "empirical_axis": {
      "pjm_assumed_utilization": 0.70,
      "ercot_metered_peak": 0.498,
      "ratio": 1.41,
      "basis": "PJM forward assumption vs ERCOT metered per-site peak / requested MW, non-crypto data centres in service 2022-2024"
    },
    "forward_axis_not_compared": {
      "pjm_accepted": 0.63,
      "pjm_firm": 0.53,
      "ercot_aurora_scenario": 0.155,
      "why_not_compared": "PJM's figure is administrative vetting; ERCOT's is a commissioned scenario model (Aurora, motive tier 3). Both are planning judgements, not measurements, so the ~4x gap between them is not evidence that either is correct."
    },
    "relationship": "single_empirical_axis_comparison",
    "do_not_misread": "Do not present the forward figures (63% vs 15%) as a cross-region empirical finding: both are modelled. Do not treat ERCOT's 49.8% as request survival. Do not use ERCOT's 15% in the section 9 bracket."
  },
```

---

### R2 — §7's 48%-vs-63% reconciliation is asserted, not derived  ★ resolve from source

**Problem.** `:102` asserts:

> The aggregate request is de-rated from ≈60 GW to ≈38 GW (≈63% survival) because the aggregate includes already-firm load (≈32 GW) that receives no probability haircut.

That is a mechanism, not a derivation, and it only holds under one of two mutually exclusive readings — one of which contradicts the table four paragraphs above it:

- **Reading A — 32 GW is firm *submitted*** (what `:98`'s "≈53% of submitted" implies). Non-firm submitted = 28 GW; accepted (38) − firm (32) = 6 GW non-firm survives; non-firm survival = **6 / 28 = 21%**, less than half the worked example's 48%. The stated mechanism is contradicted.
- **Reading B — 32 GW is firm *accepted*, post-0.70 factor.** Firm submitted ≈ 32 / 0.70 ≈ **45.7 GW**; non-firm submitted ≈ 14.3 GW; non-firm accepted ≈ 6 GW = **42%**, which sits near the worked example. Arithmetic works — but firm load is then **76% of the request**, contradicting "Firm only … ≈53% of submitted" at `:98`.

**Resolve from source. Both documents are on this machine:**

```
/home/Noel/Desktop/Reference PDFs/2_AI_Energy_Grid_and_Infrastructure/20251124-item-03---large-load-adjustment-requests-summary.pdf
    -> slides 3, 4, 7, 8, 14: the Submitted / Proposed / Firm curves
/home/Noel/Desktop/Reference PDFs/6_Academic_Papers_and_Methodology/load-adjustment-request-implementation.pdf
    -> the 2,600 -> 1,800 -> 1,260 MW worked example and the factor definitions
/home/Noel/Desktop/Reference PDFs/2_AI_Energy_Grid_and_Infrastructure/PJM Load Forecast Report 2026-01.pdf
    -> the final accepted figures
```

Establish **whether the Firm curve is plotted before or after the de-rate**, then write the actual decomposition into `:102` and correct whichever of `:98` or `:102` is wrong.

**If the decks do not state it: stop and report to Noel.** Do not pick a reading. As an interim, the following is true under *both* readings and can be stated safely — but flag in your report that R2 is unresolved:

> Of the ≈38 GW accepted for 2030, ≈32 GW is already Firm (ESO/CC-backed), leaving ≈6 GW of non-firm load inside the accepted figure. The default-probability machinery therefore governs a minority of the accepted number: the ≈63% aggregate survival is driven mainly by how much of the request was already contractually committed, not by the severity of the haircut applied to the rest. PJM does not publish the decomposition linking the aggregate to the ≈48% worked example, which is the de-rate applied to a fully non-firm request and should be read as such.

That 6-of-38 observation is worth keeping in the paper regardless of how R2 resolves: it means the 50%-probability rule §7 documents at length governs roughly 16% of the accepted figure.

---

### R7 — the two rails are denominated in different units  ★ resolve from source (round-1 A5, not done)

**Problem.** Round 1 answered this with the capacity-vs-**energy** bullet at `:158` — that was round-1 A6, a different item. The original issue is untouched:

- **Lower rail** ≈20–22% = MW-capacity In Service ÷ MW-capacity announced — a **capacity : capacity** ratio.
- **Upper rail** ≈48–63% derives from PJM curves to which a 70% capacity-to-demand factor has been applied. The worked example is explicit: "2,600 MW requested **capacity** → … 1,260 MW **demand**" (`:102`).

A capacity:capacity ratio and a demand:capacity ratio are not endpoints of one band.

**Resolve from source.** Same three PDFs as R2. Establish **whether the ≈60 GW Submitted curve is stated in requested capacity or in forecast demand** — i.e. whether the 0.70 factor is applied on top of it or already inside it. Then either restate both rails on one basis, or state the conversion explicitly.

**If the decks do not state it: stop and report to Noel**, and insert this bullet after `:144` in the interim:

> - **A note on denominators.** The two rails are not denominated identically. The lower rail is a capacity ratio (MW in service ÷ MW announced). The upper rail derives from PJM curves to which a 70% capacity-to-demand factor has been applied, so it is closer to a demand:request ratio. The envelope should therefore be read as spanning two related questions — how much requested capacity gets built, and how much requested load is accepted into a forecast — not as a confidence interval on a single quantity.

and extend `:157`'s "Two named load-bearing assumptions" bullet with:

> A third assumption is that the two rails are commensurable enough to bracket; §9 states why they are not identically denominated.

---

### R8 — WMPA sensitivity: run it  ★ the data is on this machine (round-1 A9, partly done)

**Problem.** `:68` discloses the inclusion, which is the important half:

> IA-executed includes interim Wholesale Market Participation Agreements (WMPA); excluding them shifts r2 **slightly** lower.

"Slightly" is a magnitude nobody has measured. `reproduce.py:87-90` is unchanged and `IA_EXECUTED_VALS` still contains `"Wholesale Market Participation Agreement"`.

**Run it. `reproduce.py`'s first candidate path already points at the file, which exists:**

```
/home/Noel/Desktop/Reference PDFs/AI_Energy/PlanningQueues.xlsx      (serial queue — the headline cohort)
/home/Noel/Desktop/Reference PDFs/AI_Energy/CycleProjects-All.xlsx   (cluster cohort — r1 de-dup)
```

So `python3 reproduce.py` runs as-is, no path edit needed.

**Procedure:**
1. Baseline: `python3 reproduce.py` and `python3 reproduce.py "MW Capacity"` — confirm 204.4 GW entered, 46.5 GW built, 22.8%, r2 39.1%, r3 58.1%. Capture stdout.
2. Add a proper toggle rather than a manual edit — replace the hardcoded set with:
   ```python
   IA_STRICT = os.environ.get("IA_STRICT", "0") == "1"
   IA_EXECUTED_VALS = ({"Document Posted"} if IA_STRICT else
                       {"Document Posted", "Wholesale Market Participation Agreement"})
   ```
3. `IA_STRICT=1 python3 reproduce.py` — capture r2, r3, and confirm built/entered is **unchanged** at 22.8% (it must be: the headline is built ÷ entered and does not pass the IA gate; if it moves, something else is wrong — report it).
4. Report r2 and r3 as brackets in `:65`, `:68`, `:177`, and in `claims.json` (`supply.r2.viability`, `supply.r3.build`).
5. Replace the `NOTE (C2 flag)` comment at `reproduce.py:87-89` with the measured result and the date.
6. Paste both runs' stdout into the commit message.

**Only if the run fails** (corrupt file, schema drift, missing column), report to Noel and use this interim wording, which claims no magnitude:

> IA-executed includes interim Wholesale Market Participation Agreements (WMPA), which are not full executed IAs; excluding them would lower r2 by an amount not yet quantified. The headline 22.8% is unaffected either way, since it is built ÷ entered and does not pass through the IA gate.

---

### R3 — §9's block quote still carries the deleted convergence claim

`:146` retains, verbatim from the pre-amendment draft:

> By the operators' own primary vetting, roughly half of the announced large-load ask survives to the forecast, and historical energisation is lower again.

Plural "operators'". This is the claim removed everywhere else, and under R1 it now contradicts §8 outright. Replace with:

> By PJM's own primary vetting, ≈63% of the announced large-load ask survives into the forecast and ≈53% is firm, and historical energisation on the supply side is lower again.

---

### R4 — the "≈50–63%" upper rail is orphaned

The `50` was ERCOT's 49.8%, which R1 removes from the rail entirely. The remaining PJM values are 48% (worked example), 53% (firm), 63% (accepted).

| Location | Current | Replace with |
|---|---|---|
| `:13` abstract | `≈50–63% PJM-accepted ceiling` | `≈48–63% PJM-accepted ceiling` |
| `:143` §9 bullet | `Call the upper rail ≈50–63%.` | `Call the upper rail ≈48–63%: the worked-example de-rate at the bottom, the accepted aggregate at the top.` |
| `:146` block quote | `to ≈50–63% (operator-accepted ceiling)` | `to ≈48–63% (operator-accepted ceiling)` |
| `:179` Verification note | `upper rail 50–63%` | `upper rail 48–63%` |
| `:201` version history | — | rewritten per **R15** |

In `claims.json`, `band.upper` stays `0.63`; add `"upper_low_end": 0.48` and replace `upper_basis` with:

> `"operator-accepted ceiling from PJM only (~63% accepted, ~53% firm, ~48% worked example). ERCOT contributes no figure to this rail: its 15% is a commissioned model and its 49.8% measures post-build utilization, not survival into a forecast."`

---

### R5 — `ercot_funnel.csv` has a unit bug that is live on the published site  ★ do this first

**Problem.** Round 1 added:

```
Realized per-site peak consumption,49.8,50,...
```

under the header `stage,gw,pct_of_requested,…`. A **percentage is sitting in the `gw` column**, and a **per-site rate is sitting in a column meaning "share of the 226 GW queue."**

`index.html:293` calls `loadRows(DCERCOT,'gw','pct_of_requested')`, which prints the cell verbatim. The live interactive therefore renders **"49.8 GW"** at a **50%** share with a 50%-wide bar — inviting exactly the 0.50 × 226 = 113 GW misread that `claims.json:159` forbids. The `Forecast gate requirement` row renders as literal **"null / null%"**.

`check_claims.py` passes because no claim's `csv_check` points at either row. **R13** closes that hole.

**Fix — delete both non-funnel rows from `ercot_funnel.csv`:**
- `Realized per-site peak consumption,49.8,50,…`
- `Forecast gate requirement (executed agreement),null,null,…`

Neither is a stage in a GW funnel. Both already live in `claims.json` (`load.ercot.realized_derate`, `load.ercot.forecast_gate`) and in the paper prose, which is where they belong. That leaves the three genuine stages: Requested 226 / Credible 35 / Energized 5.3. Then `python3 build.py`.

**Also in `dc_funnel.csv`:** the `PJM data-centre growth 2025-30 [benchmark subset]` row is labelled correctly in its `basis` but still renders as a funnel row with a 50% bar. Change its `stage` cell to `PJM data-centre growth 2025-30 (benchmark, not a funnel step)` so the label survives into the rendered table.

**Optional, only if the interactive must show the utilization figure:** add `row_kind` (`funnel` | `metric`) and `metric_pct` columns, and teach `loadRows` to render `metric` rows in a separate sub-table with no GW cell and no bar. That is a JS change in `index.html` plus a `build.py` re-run — do not attempt it as a CSV-only edit.

---

### R6 — §1 says the operators haircut "in private"; §7 and §10 say they publish

`:19`, added in round 1:

> The target of this deflation is not the grid operators themselves (who already apply administrative haircuts **in private**) …

contradicts `:90` ("PJM performs and publishes the announced-to-deliverable deflation itself, with a documented, reproducible method"), `:27-28` (which cites the published documents), and `:154` ("the operators deflate and publish"). The published nature of the haircut is the paper's central reproducibility asset; it cannot also be private.

Replace the parenthetical with:

> (who already apply these haircuts and publish the method)

---

### R9 — §3's attrition clause now dangles

`:68` reads:

> The largest single drop occurs between Feasibility and the System Impact Study (28pp), though attrition is spread across the three study gates (28pp at SIS, 26pp at IA, 16pp at build), **where each project learns its share of network-upgrade costs.**

The "where" clause was written for the System Impact Study; it now attaches to the three-gate list, implying costs are revealed at all three. "Build" is also not a study gate. Replace with:

> The largest single drop, 28pp, occurs between Feasibility and the System Impact Study, where each project learns its share of network-upgrade costs. Attrition is not concentrated there, however: it is spread across three gates (28pp into System Impact, 26pp into IA-executed, 16pp from IA to in service).

---

### R10 — loose ends on the headline-figure citations

- `:184` introduces **"485 to 950 TWh"**, but 485 appears nowhere in the body. Either add the baseline at `:88` ("from ≈485 TWh today to ≈950 TWh by 2030") or drop it from the Verification note.
- `:88` attributes "$850B announced data-centre leases" to **"(private-capital research)"** and `:184` to **"private-capital announcements"**. Neither names a source, so the claim is not checkable. Name the specific report and date, or reword to `the "$850B announced data-centre leases" framing circulating in private-capital commentary` — honest about being a characterisation of discourse rather than a sourced figure.

---

### R11 — **STRUCK.** "Google Gemini 3.7" confirmed correct by the author. No action in `paper_v1.md` or `zenodo_paper_v1_description.txt`.

Note the one real edit that remains in that sentence, which is grammatical: `:191` reads "The assisting **model** is not always a neutral party" while naming two vendors and then discussing both conflicts. Restore agreement:

> The assisting **models are** not always neutral **parties** to the subject matter; Anthropic is a party to …

---

### R12 — **STRUCK.** DOIs verified correct. See the verification record in §0. No action.

---

### R13 — `check_claims.py` cannot see any of the bugs it should have caught  ★ this is what ends the review cycle

**Problem.** `check_claims.py` compares `claims.json` against CSVs authored from the same claims — two of the author's own files agreeing. It has never checked the **paper prose**, where round 1's errors (B1, B2, B3) and this round's (R3, R4) live. It cannot see R5 either, because no claim points at the offending rows.

Keep the existing CSV check exactly as it is. Append three:

**(1) Prose check** — every numeric claim must appear in `paper_v1.md`:

```python
def prose_check(claims, md_path="paper_v1.md"):
    md = pathlib.Path(md_path).read_text(encoding="utf-8")
    md_norm = md.replace("≈", "~").replace("–", "-")
    missing = []
    for c in claims:
        v = c.get("value")
        if not isinstance(v, (int, float)):
            continue                     # lists / None handled separately
        pats = {f"{v:g}", f"{v:.1f}".rstrip("0").rstrip(".")}
        if not any(p in md_norm for p in pats):
            missing.append((c["id"], v))
    return missing
```

Report each miss as FAIL with the claim id. This catches the orphaned `50` (R4) and the stale "roughly half" quote (R3).

**(2) CSV unit sanity** — a GW column must contain GW, and a percent column must agree with it:

```python
def unit_check(rows, gw_key, pct_key, tol=3.0):
    problems, base = [], float(rows[0][gw_key])   # the 100% row
    for r in rows:
        if r.get("row_kind", "funnel") != "funnel":
            continue                              # metric rows opt out explicitly
        g, p = r[gw_key], r[pct_key]
        if g in ("", "null") or p in ("", "null"):
            problems.append((r["stage"], "non-numeric cell in a numeric column"))
            continue
        implied = 100 * float(g) / base
        if abs(implied - float(p)) > tol:
            problems.append((r["stage"],
                f"{gw_key}={g} implies {implied:.1f}% but {pct_key}={p}"))
    return problems
```

Run over `dc_funnel.csv` (`gw_2030`, `pct_of_submitted`) and `ercot_funnel.csv` (`gw`, `pct_of_requested`). On the *current* `ercot_funnel.csv` this flags both offending rows — 49.8 GW would imply 22%, not 50%. Non-funnel rows must carry `row_kind=metric` to be skipped; that is the point, it forces the label.

**(3) Paper ↔ passport tier agreement** — assert no claim with `motive_tier: 3` appears under a tier-1 or tier-2 heading in the Verification note. This catches the Aurora promotion (R1f) mechanically.

Update the module docstring to state what is and is not covered, and fold the new results into the summary so the "not locally checkable" list shrinks honestly.

---

### R14 — versioning: the v2 PDF relationship is still unstated (round-1 B6, partly done)

**Done in round 1:** `claims.json:215` corrected to "Treating v1 as supply-only"; version history gained both DOIs.

**Still open:** the directory contains `Contingent vs. Robust AI Power Demand — v2.pdf` dated **2026-06-25**, between v0.1 (2026-06-15) and this v1 (2026-08-16). Reading order is v0.1 → v2 → v1. `build.py:7-8` still calls the load-side CSVs "v2 load side".

1. Add to the v1 version-history entry: *"Supersedes an interim draft circulated as 'Contingent vs. Robust AI Power Demand v2' (June 2026); that title and numbering are retired, and this v1 is the first release under the current title."* — **check whether a DOI was minted against that interim draft before writing anything about it.** `zenodo_paper_v2.json` exists and carries a `--newversion` spec, which suggests a mint was at least prepared. If one was minted, relate the records instead of calling the numbering retired, and report to Noel.
2. `build.py:7-8`: "v2 load side" → "load side".
3. Rename the stray PDF to `ARCHIVE_interim_draft_2026-06-25.pdf`, or move it to an `archive/` subdirectory, so it cannot be mistaken for a current release.

---

### R15 — rewrite the version-history entry after this pass

`:201` currently claims DOIs were "standardised across all files" (they were already correct — see §0) and contains the typo **"denotates"** (→ "denotes"). Replace the amendment clause with an accurate account once R1–R14 are applied, e.g.:

> Integrates two red-team amendment passes: narrows the cross-region finding to the single axis where PJM and ERCOT are comparable like-for-like (metered 49.8% post-build utilization against PJM's assumed 70%), and demotes the modelled forward comparison to context; corrects the queue-transfer phrasing in §9; adds a tier-2 secondary-traced provenance bucket and restores the commissioned Aurora scenario to tier 3; states the observed firm/non-firm split in the PJM aggregate; names the denominator basis of the two rails; sets the upper rail to ≈48–63%; discloses WMPA inclusion with a measured sensitivity; removes non-funnel rows from the ERCOT aggregate CSV; and extends check_claims.py to cover the paper prose, CSV units, and paper-to-passport tier agreement.

Adjust the WMPA and denominator clauses to match what R8 and R7 actually resolved to, and state explicitly if either was escalated rather than resolved.

---

## §3 — Execution order

1. **R5** first — it is live on the published site — then `python3 build.py`.
2. **R1** — the framing change; touches abstract, §8, §9, Verification note, `claims.json`.
3. **R3, R4, R6, R9, R10, R11-grammar** — mechanical prose fixes.
4. **R8** — run the sensitivity against `PlanningQueues.xlsx`.
5. **R2, R7** — open the three PJM PDFs and resolve. Escalate rather than invent.
6. **R13** — extend `check_claims.py`, run it, fix whatever it surfaces.
7. **R14, R15** — versioning and history.
8. Regenerate `paper_v1.html` and `paper_v1.pdf`.

---

## §4 — Escalation

Report back to Noel, rather than proceeding, if any of these occur:

- The PJM decks do not state whether the Firm curve is pre- or post-de-rate (**R2**), or whether the Submitted curve is capacity or demand (**R7**).
- `reproduce.py` fails to run, or the headline 22.8% moves under `IA_STRICT=1` (**R8**) — it should not; built ÷ entered does not pass the IA gate.
- A DOI was minted against the June interim draft (**R14**).
- `check_claims.py`'s new checks surface a mismatch you cannot resolve without changing a published figure (**R13**).

In each case: state what you found, what you could not settle, and stop that item. Complete every other item.

---

## §5 — Pre-mint checklist

- [ ] `python3 check_claims.py` exits 0 **with R13's three new checks active**
- [ ] `ercot_funnel.csv` and `dc_funnel.csv` contain only funnel stages, or non-funnel rows carry `row_kind=metric` and render separately
- [ ] `python3 build.py` re-run; `index.html` ERCOT table shows no "49.8 GW" and no "null%"
- [ ] Upper rail reads ≈48–63% in all four prose locations plus `claims.json`
- [ ] `grep -n "roughly half" paper_v1.md claims.json` → no hits
- [ ] `grep -n "in private" paper_v1.md` → no hits
- [ ] `grep -n "both comparable axes\|empirical divergence" paper_v1.md claims.json` → no hits
- [ ] Aurora under tier 3 in the Verification note **and** `motive_tier: 3` in `claims.json`; no tier-3 claim sits under a tier-1/2 heading
- [ ] R8 sensitivity run, both stdout captures in the commit message, `reproduce.py` C2-flag comment replaced with the measured result
- [ ] R2 and R7 either resolved from the PJM decks (with the finding recorded) or escalated (with the interim text in place and the escalation noted in the version history)
- [ ] `_target_record_caveat` in `zenodo_paper_v1.json:3` still present and unresolved — **Noel must confirm the record id before `--newversion`**
- [ ] `paper_v1.html` / `paper_v1.pdf` regenerated; `pdfinfo paper_v1.pdf` title correct
- [ ] Version history rewritten per R15, stating which items were escalated
- [ ] DOI minted **last**, and only after Noel answers the record-id question

---

## §6 — Do not change

The supply-side core survived both passes intact: 22.8% reconciles exactly (46.5 / 204.4), the r2 × r3 identity is correctly labelled as an identity rather than sold as a consistency check, the MW-Capacity robustness run (24.8%) is disclosed, In-Service-only genuinely biases the rate down, the cohort-maturity trap is handled properly, and §5's finding that inflation is withdrawal-driven rather than duplication-driven argues against the author's own stated prior.

Round 1's fixes listed in §1 are correct as applied — do not revert them. In particular keep: the §9 "separate queues" phrasing, the tier-2 provenance bucket, the reworded Guarantee, the 3.2pp under-construction disclosure, the 39.1% correction, the %withdrawn footnote, and the concept-DOI citations.

The `do_not_misread` discipline in `claims.json` is the most valuable thing in the repo. Preserve every existing entry verbatim, and add one for every claim this pass changes.
