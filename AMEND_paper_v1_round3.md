# Amendment note #3 — *Announced vs. Deliverable AI Power Demand* (v1)

**To:** implementing agent
**From:** red-team pass #3, 2026-08-16
**Scope:** delta only. Rounds 1 and 2 are complete and verified — see §1. This note has **seven items**, five of them sourced directly from the PJM deck.
**Source of record:** `paper_v1.md` as of 13:31, 2026-08-16.

**Primary document used for this pass (on this machine):**
```
/home/Noel/Desktop/Reference PDFs/2_AI_Energy_Grid_and_Infrastructure/20251124-item-03---large-load-adjustment-requests-summary.pdf
```
33 pages. Extract with `pdftotext -layout`. Slide numbers below are the deck's own footer numbers.

**Also on this machine, needed for R18:**
```
/home/Noel/Desktop/Reference PDFs/2_AI_Energy_Grid_and_Infrastructure/PJM Load Forecast Report 2026-01.pdf
```

---

## §0 — Rules of engagement

1. **R16 and R17 are sourced, not inferred.** Verbatim quotes and slide numbers are given. Open the deck and confirm each before writing — do not take this note's transcription on trust.
2. **Escalate, do not invent** (unchanged from round 2). If a document does not say what this note claims, stop that item and report to Noel with what you actually found.
3. Propagation rule unchanged: `paper_v1.md` → `claims.json` → CSVs → `python3 build.py` → regenerate `paper_v1.html` / `paper_v1.pdf`.
4. `python3 check_claims.py` must exit 0 with all four check groups active.
5. **R16 adds a deflation step the paper is currently missing.** It strengthens the argument. Do not soften it to protect the existing text.

---

## §1 — Round-2 ledger

**Verified complete and correct — do not revisit:** R1 (cross-region narrowed to the empirical axis; abstract, §8, §9, tier move, `claims.json` all consistent), R3, R4 (48–63% in all five locations), R5 (`ercot_funnel.csv` is three genuine funnel rows; no unit bug renders), R6, R9, R10, R11-grammar, R13 (four check groups live and passing).

**R8 verified as a genuine run, not an assertion.** The reported figures reconcile exactly: 77.7 / 204.4 = 38.0%, 46.5 / 77.7 = 59.8%, and the headline is unmoved at 22.8% as predicted. The `IA_STRICT` env toggle is correctly implemented at `reproduce.py:91-93`. Good.

**R12, R11 struck in round 2 and correctly left alone.**

**Open, and addressed here:** R2 was answered by assertion rather than from the deck (→ **R16**); R7 was left hedged when the deck settles it (→ **R17**); R14 was half-applied (→ **R20**).

---

## §2 — The items

### R16 — §7 is missing a third haircut step that PJM documents  ★ new sourced finding

**What the deck says.** Slide 6, *Discounting "Non-Firm"*, verbatim:

> • Levels of "Non-Firm" were significantly beyond what could fit into a top-down framework.
>   – Implementation document used to conform "Non-Firm" requests to ramp and utilization guidelines
>   – **"Non-Firm" was then further reduced to reflect National constraints**

And on roughly ten of the per-EDC slides, the annotation recurs almost verbatim. PL (slide 14) and JCPL (slide 21):

> • Non-Firm prior to 2030 equal to zero and 2030+ applied **50% and national average scaling**

PS (slide 18):

> • Non-Firm prior to 2030 equal to zero and 2030+ already had 50% applied in submitted data.
> • **Applied national average scaling for 2030+**

**Why it matters.** PJM's non-firm treatment is **three** multiplicative steps, not two:

1. 50% default probability (or an EDC/LSE-supplied factor)
2. ramp and utilization conformance per the Implementation document — this is where the ≈48% worked example ends
3. **national average scaling** — applied *after* step 2, and nowhere in §7

That third step is the missing explanation for the gap §7 currently papers over. The paper's own aggregate arithmetic gives non-firm survival of 6/28 ≈ 21% at 2030, against a worked example of ≈48%. The residual, ≈21/48 ≈ **0.44**, is national average scaling. §7 currently attributes the whole 63%-vs-48% gap to firm load escaping the probability haircut, which is incomplete: firm load escapes the *probability* factor, but the reason non-firm lands at 21% rather than 48% is step 3.

Note `dc_funnel.csv`'s Proposed row already lists "national scaling" in its `basis` field. The project knew; §7 does not say it.

**A second fact worth having.** "Non-Firm prior to 2030 equal to zero" — for several EDCs PJM zeroes non-firm large load entirely before 2030. That is a harder screen than anything §7 currently describes and it points the same way as the rest of the paper.

**Fix — replace the reconciliation sentences at `:102`.** Currently:

> The aggregate 2030 request is de-rated from ≈60 GW to ≈38 GW (≈63% survival) because the aggregate includes already-firm load (≈32 GW, or ≈53% of submitted request) that receives no probability haircut. Of the ≈38 GW accepted for 2030, ≈32 GW is Firm (ESO/CC-backed), leaving ≈6 GW of non-firm load surviving inside the accepted figure (a 6/28 ≈ 21% non-firm survival rate in 2030). The default-probability machinery therefore governs a minority of the accepted number: the ≈63% aggregate survival is driven mainly by how much of the request was already contractually committed, not by the haircut applied to the rest.

Replace with:

> Non-firm requests pass three multiplicative screens, not two. PJM applies the default 50% probability; then conforms the request to the Implementation document's ramp and utilization guidelines; and then reduces it again, in PJM's words, "to reflect National constraints" — the per-EDC slides record this as "50% and national average scaling," and for several EDCs non-firm load before 2030 is zeroed outright. The published worked example covers only the first two screens. That is why the aggregate is not a simple application of it: of the ≈60 GW submitted for 2030, ≈32 GW is already Firm and passes without a probability haircut, while the ≈28 GW of non-firm survives to ≈6 GW inside the ≈38 GW accepted — a ≈21% non-firm survival rate, against the ≈48% the worked example alone would give. The residual, a factor of roughly 0.44, is the national-scaling step. Two things follow. The ≈63% aggregate is driven mainly by how much of the request was already contractually committed rather than by the severity of the haircut on the rest; and the deflation PJM actually applies to uncommitted load is materially steeper than its own documented worked example implies.

**Then update:**
- `:102`'s haircut-mechanics list — add national average scaling as a fourth named mechanic alongside the 50% probability, the 70% factor and the 36-month ramp.
- Verification note `:175` — add the national-scaling step and its slide references to the tier-1 PJM Load Side bullet.
- `claims.json` `load.pjm.worked_example_survival.uncertainty` — currently "Applied de-rate = probability ~0.69 x utilization 0.70." Append: `The worked example omits the national-average-scaling step PJM applies to non-firm after conformance; aggregate non-firm survival at 2030 is ~21%, implying a scaling factor of ~0.44.`
- Add a new `known_misreads` entry: `"Treating PJM's ~48% worked example as the rate PJM actually applies to non-firm load in aggregate: the worked example omits the national-scaling step, and realized non-firm survival at 2030 is ~21%."`

---

### R17 — §9's denominators bullet can be upgraded from hedge to sourced statement

**What the deck says.** Utilization is applied to the *whole* submission, Firm included, by the submitting EDC. BGE (slide 10):

> • CC and financial deposit for all submitted projects considered Firm.
> • **Exelon's submission used a 70% utilization rate for each data center's requested capacity.**

PL (slide 14), with the same construction:

> • Projects with ESA considered Firm. • Projects with LOA considered Non-Firm.
> • **Used 70% utilization rate for each data center's requested capacity.**

And slide 4, *Evaluating Requests*:

> • Investigated utilization rate (% of final capacity that is used) and **imposed 70% unless otherwise supported**

**What this settles.** The Firm and Proposed curves are **demand-basis**, after the 70% capacity-to-demand conversion. The Submitted / Request curve is **requested capacity**. So the ≈63% and ≈53% ratios are demand ÷ requested-capacity, while the lower rail is capacity-in-service ÷ capacity-announced. The denominator mismatch flagged in round 2 is **confirmed**, not merely possible.

**Fix — replace the `:148` bullet.** Currently it says the upper rail "is closer to a demand:request ratio" and leaves it open. Replace with:

> - **A note on denominators.** The two rails are not denominated identically, and PJM's own documentation settles which is which. The 70% capacity-to-demand factor is applied to every submitted project, Firm included: PJM "imposed 70% unless otherwise supported," and the EDC submissions record a "70% utilization rate for each data center's requested capacity." The Proposed and Firm curves are therefore stated in forecast demand, while the Submitted curve is stated in requested capacity, so the upper rail is a demand ÷ requested-capacity ratio. The lower rail is a capacity ratio (MW in service ÷ MW announced). Read the envelope as spanning two related questions — how much requested capacity gets built, and how much requested load is accepted into a forecast — not as a confidence interval on one quantity. On a common capacity basis the upper rail would be higher by roughly the reciprocal of 0.70; the band is reported on the operators' own published basis rather than restated, and this is the softest joint in it.

Mirror in `claims.json` `band.note`, and in `:161`'s third-assumption clause (change "§9 states why they are not identically denominated" to "§9 states, from PJM's documentation, how each is denominated").

---

### R18 — the three headline PJM load figures are chart reads, labelled as transcriptions  ★

**Problem.** The 60 / 38 / 32 GW figures are the load side's headline numbers. The Verification note files them under **"Traced to official operator records and filings (tier 1)"** and `claims.json` marks all three `"reproducibility": "transcribed"` — defined in the tier legend as *"transcribed verbatim from a cited primary operator document."*

They are not. Slides 7 and 8 of the LAS deck are **unlabelled bar charts**: the only printed numbers are axis gridlines (0 / 20,000 / … / 140,000 MW) and the series legends (`Submitted`, `Proposed`, `2025LF`; `RTO Total - Firm`, `RTO - Total Non-Firm`, `RTO - Request`). No data labels, no table. The values were read off a chart, which is an estimate, not a transcription.

`dc_findings.md:84` records the author already knew this: *"Optional precision still open: pull exact PJM B-9/B-9b GW-by-year from the Excel supplement for a single headline figure."*

**Fix — preferred.** Pull the exact 2030 values from `PJM Load Forecast Report 2026-01.pdf` (on this machine; look for the B-9 / B-9b large-load adjustment tables), or from the LTLF Excel supplement if the report only charts them. Replace the ≈ figures with the printed ones and keep `transcribed`.

**Fix — if the exact values are not printed anywhere.** Add a fourth reproducibility tier to the legend in `claims.json`:

```json
"chart_read": "read from an unlabelled chart in a cited primary operator document; an estimate, not a transcription"
```

retag `load.pjm.submitted_2030`, `load.pjm.accepted_2030` and `load.pjm.firm_2030` as `chart_read`, and add to the Verification note's tier-1 PJM Load Side bullet: *"The 60 / 38 / 32 GW 2030 values are read from the unlabelled bar charts on slides 7 and 8; PJM does not print them. They are stated to the nearest GW and should be treated as chart reads."*

The paper already hedges every use with ≈, so nothing downstream breaks. This is about the Guarantee at `:198` being literally true.

---

### R19 — verify the AEP claim against its own slide

`:102` ends: *"AEP's submission was de-rated by more than 50%."* The AEP slide is **13** in the deck (its legend reads `AEP - Firm | AEP - Non-Firm | AEP`). Confirm the claim against that slide specifically — during this pass the annotation block adjacent to the AEP legend resolved to the PL slide (14) under `pdftotext -layout`, so the attribution has not been independently checked. If the AEP slide does not support "more than 50%," correct or drop the sentence.

---

### R20 — round-2 housekeeping half-applied

**(a) The interim draft was copied, not renamed.** Both files are present and identical in size (160,192 bytes):

```
ARCHIVE_interim_draft_2026-06-25.pdf          (created 13:30 today)
Contingent vs. Robust AI Power Demand — v2.pdf (original, 25 Jun)
```

The confusing filename is still in the directory, so the problem R14 existed to solve is unsolved and there is now a duplicate. Delete `Contingent vs. Robust AI Power Demand — v2.pdf` after confirming the two are byte-identical (`cmp` them first).

**(b) The version history misquotes the draft it retires.** `:206` says:

> Supersedes an interim draft circulated as 'Contingent vs. **Deliverable** AI Power Demand v2' (June 2026)

The actual title is *Contingent vs. **Robust** AI Power Demand — v2*. Correct it. A wrong title in the sentence retiring a title is the kind of thing a reader checks.

**(c) The DOI question from R14 is still unanswered.** `zenodo_paper_v2.json` exists with a `--newversion` spec, which suggests a mint against the interim draft was at least prepared. Confirm with Noel whether one went out before asserting the numbering is retired.

---

### R21 — r2 is a point in the table and a bracket in the Verification note

`:65` gives `Reached IA-executed | 39.1% (= r2)`. `:181` now correctly gives `r_2 = 38.0-39.1%` depending on WMPA inclusion, and `:68` explains it. `claims.json` `supply.r2.viability` carries the point value 39.

Add a footnote under the funnel table so the table does not read as more precise than the Verification note:

> *\*r2 on the headline basis, which includes interim WMPAs; excluding them gives 38.0%. See §3 text and the Verification note.*

Leave `claims.json`'s value at 39 (R13's prose check matches against the paper, and 39.1 appears at `:65`), but extend its `uncertainty` field to name the 38.0–39.1% bracket.

---

### R22 — version history

After R16–R21, update `:206`. Beyond the title correction in R20(b), the entry should record the two substantive additions from this pass:

> …identifies the national-average-scaling step PJM applies to non-firm load after ramp and utilization conformance, and restates the aggregate-versus-worked-example gap accordingly; establishes from PJM's documentation that the Proposed and Firm curves are demand-basis while Submitted is requested capacity, and states the resulting denominator asymmetry in the two-rail envelope…

If R18 resolves to `chart_read` rather than exact figures, say so there too.

---

## §3 — Execution order

1. **R16** — the substantive addition. Confirm slides 6, 14, 18, 21 first.
2. **R17** — confirm slides 4, 10, 14, then rewrite the `:148` bullet.
3. **R18** — try `PJM Load Forecast Report 2026-01.pdf` for exact values; fall back to the `chart_read` tier.
4. **R19** — check slide 13.
5. **R20, R21, R22** — housekeeping, footnote, history.
6. `python3 build.py`; re-run `check_claims.py`; regenerate `paper_v1.html` / `paper_v1.pdf`; `pdfinfo` the title.

---

## §4 — Escalate to Noel if

- Slide 6 or the per-EDC slides do not carry the national-scaling language as quoted (**R16**) — the whole item falls if so.
- The 2026 LTLF report and its supplement print no exact 2030 large-load values, so R18 has to take the `chart_read` route — say so explicitly rather than leaving the tier as `transcribed`.
- The AEP slide does not support "de-rated by more than 50%" (**R19**).
- A DOI was minted against the June interim draft (**R20c**).

---

## §5 — Do not change

Everything listed as verified in §1. In particular do not reopen the cross-region framing (R1), the WMPA sensitivity (R8), the ERCOT CSV structure (R5), or the DOI citations — all four are settled and correct.

The supply-side core remains untouched across three passes and should stay that way: 22.8% = 46.5 / 204.4, the r2 × r3 identity correctly labelled, the MW-Capacity robustness figure disclosed, In-Service-only biasing the rate down, and §5's withdrawal-not-duplication finding arguing against the author's own prior.
