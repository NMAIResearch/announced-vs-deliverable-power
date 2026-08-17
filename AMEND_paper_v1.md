# Amendment note — *Announced vs. Deliverable AI Power Demand* (v1)

**To:** implementing agent
**From:** red-team pass, 2026-08-16
**Source of record:** `paper_v1.md` (line numbers below refer to it; `paper_v1.pdf` / `paper_v1.html` are derived and match)
**Status:** findings only — nothing has been edited. Do not start until §0 is read.

---

## 0. Rules of engagement

1. **Do not touch §3, §4, §5 or `reproduce.py`'s core logic** except where item **A5** and **B4** name a specific line. The supply side reconciles exactly (46.5/204.4 = 22.75% → 22.8%) and is the strongest part of the paper. Leave it alone.
2. **Items in Group A change what the paper concludes.** Do not apply them silently — each one has a decision attached, marked **[AUTHOR CALL]**. Draft the replacement text, flag the call, wait.
3. **Items in Group B and C are mechanical.** Apply them.
4. Every figure that changes must be changed in **all** of: `paper_v1.md`, `claims.json`, the relevant CSV, and `index.html` (via `python3 build.py`). `check_claims.py` must still exit 0.
5. **Rebuild path warning:** `build.py` only re-embeds the CSVs into `index.html`. It does **not** regenerate `paper_v1.html` or `paper_v1.pdf` from `paper_v1.md` — that pipeline is external (the PDF was printed from HeadlessChrome). Confirm the regeneration command with the author before re-minting, and re-run `pdfinfo` to check the title metadata survives.
6. Do not re-mint a DOI until Group A is resolved. Group A changes a headline result.

---

## Group A — substantive; changes the conclusion

### A1. The ERCOT number used in the cross-region result is the wrong one of three

**Where:** abstract (`:13`), §8 cross-region table (`:132-137`), §9 upper rail (`:143`), `claims.json` `cross_region` block (`:195-201`), `band.upper_basis` (`:206`).

**The problem.** §8 (`:122-126`) correctly separates three ERCOT quantities and warns they must not be conflated. It then conflates them:

- ERCOT **request survival** = 35 GW ÷ 226 GW ≈ **15%**
- ERCOT **realized utilization**, explicitly "conditional on the project existing" = **49.8%**

The 49.8% is placed in a column headed "First-screen survival" (`:134-135`) and in the "operator-accepted into the forecast" rail (`:143`). Both are request-survival slots. The matching ERCOT figure — 15% — is computed two paragraphs earlier and then not used. It sits *below* the paper's own 20% floor.

**Why it matters.** The ~50% convergence is an artifact of comparing a two-factor product to one of its factors:

| Axis | PJM | ERCOT | Direction |
|---|---|---|---|
| Request survival | 63% (53% firm) | **15%** | ERCOT ~4× more deflationary |
| Utilization | 70% (assumed) | **49.8%** (realized) | ERCOT ~1.4× more deflationary |
| Compound | 0.69 × 0.70 = **48%** | 0.15 × 0.498 ≈ **7.7%** | not comparable |

On both like-for-like axes ERCOT is materially *more* pessimistic than PJM. The existing caveat ("constructed differently", `:13`, `:137`) discloses the mismatch but does not license using the number in the slot where the matched number exists.

**[AUTHOR CALL]** Two routes:

- **(a) Recommended — reframe as divergence.** Replace the "convergence" finding with: *ERCOT's realized data undercuts PJM's forward assumptions on every comparable axis.* Cross-region table becomes two rows per operator (request survival; utilization), with ERCOT lower in both. This is a stronger, falsifiable finding and it survives the objection. It costs the paper its neat "two operators, one number" headline.
- **(b) Minimal — demote the comparison.** Keep 49.8% but strip it of survival framing: rename the table column to "de-rate applied at the named step", state ERCOT's request survival as 15% in the same table, and remove 49.8% from the §9 upper rail entirely.

Either way, **§9's upper rail must lose "ERCOT: a realized ≈50% per-site"** (`:143`). The upper rail then rests on PJM alone (50–63%), which must be said.

Also update `claims.json:200` `do_not_misread` — it currently forbids exactly what the paper does.

### A2. §9 contradicts §7 on the load-bearing transfer argument

**Where:** `:144` vs `:90`.

- §7 (`:90`): "Data centres connect as load, not generation. **They do not flow through the generation queue §3 measured.**"
- §9 (`:144`): the proxy transfers because "generation and load clear the **same** interconnection queue, network-upgrade-cost gate, and equipment lead times."

Both sentences are in the shipped PDF. The §9 claim is the sole justification for the 20% lower rail.

**Fix (mechanical, no author call):** in `:144`, replace

> (generation and load clear the *same* interconnection queue, network-upgrade-cost gate, and equipment lead times)

with

> (generation and load are gated by the same network-upgrade-cost exposure, the same transformer and switchgear lead times, and the same congested interconnection points, though they clear separate queues)

The argument survives; the false claim does not.

### A3. Provenance: the Verification note claims tier 1 for figures `claims.json` says are secondary

**Where:** paper §2 (`:25`, `:32`), Verification note heading (`:168`) and ERCOT bullet (`:171`), the Guarantee (`:190`); vs `claims.json:31` and the four ERCOT claims' `"reproducibility": "secondary"`.

`claims.json:31` states plainly that ERCOT's CDN blocked direct fetch and that 226 GW, 49.8%, 5,302 MW and the PGRR115 gate came from Belfer Center / Utility Dive / Latitude Media / WECC. The paper files all four under **"Traced to official operator records and filings (tier 1)."** The closing Guarantee — "every measured claim is traced to the primary document named in the Verification note" (`:190`) — is therefore false as written for those four.

**Fix (mechanical):**
1. Add a third Verification-note bucket between tier 1 and "Derived": **"Traced via a named secondary to a named primary (tier 2)."** Move the four ERCOT bullets into it, keeping the ERCOT document names and adding the secondary that carried each.
2. Amend §2 (`:30`) — "ERCOT: … all public" → note the access path.
3. Amend the Guarantee (`:190`) to: *"every measured claim is traced to the document named in the Verification note, at the tier stated there."*
4. **Motive tiers are inconsistent with the paper's own legend.** All four ERCOT claims carry `motive_tier: 1` ("primary filing or regulator") while sourced from trade press. PJM's 50%/70%/70% constants also carry tier 1 though they are operator-chosen administrative assumptions — the legend's own definition of tier 2 ("operator/issuer self-report"). Re-tier both sets.
5. **Knock-on:** "motive-neutral referee" (`:13`, `:154`) over-claims once (4) is honest — the evidence base is two operators' self-selected constants. Soften to "referee independent of the announcing parties" or defend it explicitly.

### A4. Cherry-picking between PJM's 48% and 63%

**Where:** `:134` (48% used for cross-region) vs `:143` (63% used for the upper rail).

The aggregate haircut is 60 → 38 GW = 63%; the documented worked example is 48%. The paper uses whichever end suits the argument and never reconciles the 15pp gap. `dc_funnel.csv` hints at causes (national scaling, min 36-month ramp, firm load not de-rated) but the paper does not.

**[AUTHOR CALL]** Either (a) add two sentences in §7 explaining why the aggregate is looser than the method's worked example, or (b) pick one figure and use it in both places. Leaving both unreconciled is the one option a referee will not accept.

### A5. The two rails are denominated in different units

**Where:** §9 (`:143-146`), `claims.json` `band` block (`:202-208`).

- Lower rail: MW-capacity In Service ÷ MW-capacity announced — a **capacity:capacity** ratio.
- Upper rail: derived from figures that have already had PJM's ×0.70 capacity-to-demand factor applied. The paper's own worked example says so: "2,600 MW requested **capacity** → … 1,260 MW **demand**" (`:102`).

A capacity:capacity ratio and a demand:capacity ratio are not endpoints of one band.

**[AUTHOR CALL]** Decide which side of the meter the band is denominated in, state it in the §9 block quote (`:146`), and reconcile. If the answer is "requested capacity" throughout, the lower rail is fine and the upper rail needs its units named; if "delivered demand", the lower rail needs a load-factor adjustment.

### A6. The headline being deflated is in TWh; everything measured is in GW

**Where:** §7 (`:88`), and the same figure in `reproduce.py:257`.

The paper targets "the ≈950 TWh-by-2030 trajectory" but measures only capacity. Applying a 20–63% capacity band to an energy forecast needs a load-factor bridge, and data centres run at high load factors, so the energy haircut is not the capacity haircut.

Separately: **≈950 TWh and "$850B announced data-centre leases" are the only two figures in the paper with no citation anywhere**, including the Verification note. They are the numbers the paper exists to deflate.

**Fix:** cite both, and add one sentence to §10 Limitations stating that the band is a capacity band and does not transfer to an energy forecast without a load-factor assumption.

### A7. PJM's published forecast barely moved — name the strawman

**Where:** §7 (`:104`), §1 (`:19`).

The revisions cited are −1.6%, −2.6%, −0.8%. The thesis is that forecasts treat announced capacity as firm, but PJM's forecast already applied the haircut and net moved 1–3%, not 37–47%. The submitted-vs-accepted gap was never in anyone's published baseline.

This is compatible with the "contribution is the packaging" hedge, but a referee will ask who is actually quoting 60 GW as a forecast.

**Fix:** one sentence in §1 or §7 naming the audience the deflation is aimed at (press, private-capital announcements, lease headlines) and stating explicitly that PJM's own forecast is *not* the target. Strengthens the paper; costs nothing.

### A8. "Dominant attrition at the System Impact Study" is a 28pp vs 26pp margin

**Where:** §3 (`:68`), §4 (`:74`).

From `funnel.csv`: Feasibility→SIS drops 28pp, SIS→IA drops 26pp, IA→built drops 16pp. Attrition is roughly even across three gates. §4's grid-not-balance-sheet argument rests on the cost-reveal gate being *dominant*.

**Fix:** downgrade "the dominant attrition" / "the steepest drop" to "the largest single drop, though attrition is spread near-evenly across the three study gates (28pp / 26pp / 16pp)". The §4 argument still holds — two of the three gates are grid-driven — but state it that way rather than resting on a 2pp margin.

### A9. Undisclosed known-suspect definition in `reproduce.py`

**Where:** `reproduce.py:92-95`, surfaced in paper §3 (`:66-68`) and §4.

The author's own code comment: `IA_EXECUTED_VALS` includes `"Wholesale Market Participation Agreement"`, which "is an interim arrangement, not a full executed IA → **may over-count r2**", left in "for v0.1 continuity; flagged for a v0.2 sensitivity."

The headline 22.8% is immune (it is built ÷ entered). But **r2 = 39%, r3 = 58%, and "61% of announced MW exit before a signed agreement" are all exposed** — and those are what §4's argument rests on. The paper claims "modelled or estimated inputs are identified as such" (`:190`); this one is identified nowhere outside the code.

**Fix — preferred:** run the sensitivity (re-run `reproduce.py` with `IA_EXECUTED_VALS = {"Document Posted"}`) and report r2/r3 as a bracket. **Fallback:** disclose the choice and its direction in §3 and in `claims.json` `supply.r2.viability.uncertainty`.

### A10. The loose de-dup key is not a duplicate test

**Where:** §5 (`:80`), `reproduce.py:218`.

`loose_keys = ["Developer", "State", "County"]` collapses every project one developer has in one county down to the largest. Three genuinely distinct solar farms in one county read as two duplicates. So "literal duplicate filings remove only ≈8–19%" is mislabelled at the top end; the literal figure is ~8% (the strict key).

Note this makes the paper's conclusion **stronger** — inflation is even less duplication-driven than stated. Free win.

**Fix:** relabel the range in §5 and in `claims.json:83` as "≈8% on a literal-duplicate key, rising to ≈19% under a deliberately over-broad developer-county collapse that also absorbs genuinely distinct projects; the literal finding is the 8%."

---

## Group B — arithmetic and internal consistency; apply directly

### B1. "A further 13% exit after a signed agreement" does not reconcile — `:68`

IA-executed 39% − built 22.8% = **16.2pp**, not 13%. As written, 61% + 13% = 74%, implying 26% built.

Traced to `reproduce.py:183`: `post = reachIA − (built | advanced)`, so 13% is *IA-executed, unbuilt, and not under construction*, with ~3.2pp under construction absorbing the gap.

Two errors. **Fix:** "A further 13% of entered MW hold a signed agreement but are neither in service nor under construction, with ~3.2% still under construction." Drop "exit" — those MW have not exited.

### B2. The 70% factor is described twice but applied once — `:102`

"a 70% utilization rate **and** a 70% capacity-to-demand factor are imposed", but the worked example applies one (1,800 → 1,260). Two would give 882 MW = 34%, not 48%. `claims.json:126` lists only one ("probability ~0.69 x utilization 0.70").

**Fix:** check the PJM Implementation document (1 Jul 2025) and either merge the two descriptions into the single factor actually applied, or explain why the worked example applies only one.

### B3. Rounding drift in the Verification note — `:174`

80.0 / 204.4 = **39.14%** → 39.1%, not the stated 39.2%. Either publish the unrounded GW figures or correct to 39.1%.

### B4. `reproduce.py` ships a stale "DO NOT publish" blocker — `reproduce.py:22-25`

> `>>> RE-RUN REQUIRED before re-minting: the headline (16-25%, r2, r3, 23.3%) must be re-confirmed … DO NOT publish v0.1 figures until this script has been run against the data.`

It evidently *was* re-run — 23.3% → 22.8% matches the predicted <1pp shift — but the warning is stale and a reviewer opening the script reads it as an unresolved blocker on the headline. **Fix:** replace with a resolved note recording the outcome and the run date. Also: the script self-identifies as **v0.1** throughout a v1 release (docstring `:3`, banner `:248`); update.

### B5. Three different DOIs for the bot-energy methods precedent

- `claims.json:11` → `10.5281/zenodo.20512703`
- `reproduce.py:10` → `10.5281/zenodo.20562696`
- `reproduce.py:18` → records `20512704` as the *wrong* one it corrected

`claims.json` carries a one-digit variant of the known-bad DOI. Paper §11 (`:162`) cites the bot-energy paper with **no DOI at all**.

**Fix:** resolve the correct DOI against Zenodo, set it in all three places, and add it to §11 so a reader can follow the lineage claim.

### B6. Version numbering is incoherent, and DOIs are involved

This is **v1** dated 2026-08-16. The directory holds `Contingent vs. Robust AI Power Demand — v2.pdf` dated 2026-06-25. Version history says v0.1 was 2026-06-15. Reading order is v0.1 → v2 → v1.

Also `claims.json:215` carries a known-misread entry — *"Treating v2 as supply-only (v2 covers both supply and load)"* — inside a **v1** passport. `build.py:7-8` likewise calls the load-side CSVs "v2 load side".

**Fix:** decide the canonical sequence, correct `claims.json:215` and `build.py:7-8`, and state the relationship to the June v2 PDF in the version history. Get this right before minting — it is a citation-integrity problem, not cosmetics.

### B7. `check_claims.py` verifies less than its docstring implies

It confirms `claims.json` matches CSVs derived from the same claims — two author-written files agreeing. It never checks the **paper prose** against either, which is why B1, B2 and B3 all pass clean at exit 0.

**Fix:** amend the docstring to say what it does not cover, and — better — extend it to grep the headline figures out of `paper_v1.md` and diff them against `claims.json`. That is the check that would have caught three of the four items in this group.

---

## Group C — minor; apply if touching the surrounding text

- **C1 — `:50-54`.** The cohort table's three columns are not exhaustive (2015-17: 20 + 71 = 91 ≠ 92). `reproduce.py:145` prints the caveat that `%withdrawn` counts `Status=='Withdrawn'` only, with Retracted / Canceled / Deactivated sitting in `%resolved`. The paper drops it. Restore as a table footnote.
- **C2 — `dc_funnel.csv` row 3.** "PJM data-centre-specific growth 2025-30, 30 GW, 50%" is a data-centre-only quantity inside an all-large-load funnel, and its 50% invites reading data centres as half the funnel. Move it out of the funnel or mark it as a sidebar row.
- **C3 — `:148`.** "ERCOT's ≈2% energized-to-date sits below even the floor … a reminder that the lower rail is conservative" is a non sequitur — an age artefact carries no information about the floor's conservatism. Delete the final clause; the age-artefact point stands on its own.
- **C4 — `:116`.** 226 GW and 233 GW are both given for the same quantity at the same date. Disclosed, but state which is the queue and which is the board figure.
- **C5 — `claims.json:10`.** The v0.1 *record* DOI (20706509) appears in the passport but not in the paper's version history (`:199`), which gives only the concept DOI. Add it.

---

## Checklist before re-mint

- [ ] Group A resolved with the author; A1, A4, A5 decisions recorded in the version history
- [ ] All changed figures propagated: `paper_v1.md` → `claims.json` → CSVs → `python3 build.py`
- [ ] `python3 check_claims.py` exits 0
- [ ] `reproduce.py` re-run against the PJM export if A9 is taken; outputs pasted into the commit message
- [ ] `paper_v1.html` / `paper_v1.pdf` regenerated (confirm the pipeline — **not** `build.py`), title metadata verified with `pdfinfo`
- [ ] Version history gains a v1.1 entry listing every corrected figure
- [ ] DOI minted **only** after the above

---

## Do not change

The supply-side core is the strongest part of the paper and survived the pass intact: 22.8% reconciles exactly, the r2 × r3 identity is correctly labelled as an identity rather than sold as a consistency check, the MW-Capacity robustness run (24.8%) is disclosed, In-Service-only genuinely biases the rate down, the cohort-maturity trap is handled properly, and §5's finding that inflation is withdrawal-driven rather than duplication-driven argues against the author's own stated prior. The `do_not_misread` discipline in `claims.json` should be preserved verbatim and extended to any new claim.
