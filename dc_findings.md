# Contingent vs Robust — v2 increment: the PJM data-centre LOAD filter

**Working doc. PRIMARY SOURCES LOCKED 2026-06-25** against three PJM documents:
- *Load Adjustment Request Implementation* (PJM Resource Adequacy Planning, 1 Jul 2025) - the method.
- *Load Adjustment Requests Summary for 2026 Load Forecast - Preliminary* (LAS, Molly Mooney, 24 Nov 2025) - the numbers.
- *2026 Long-Term Load Forecast Report* (Jan 2026) - the final accepted figures (final-number lock pending; see end).

v0.1 (DOI 20706509) measured the PJM *generation* queue: ~22.8% of entered MW reach commercial operation. This increment points the same announced-vs-deliverable discipline at **data-centre LOAD** - the variable behind the "$850B announced data-centre leases" headline.

## The key structural difference (why the method changes)

Data centres connect as **load**, not generation, so they do not flow through the generation queue v0.1 measured - and the large-load process is **new** (the surge began 2024-25), so **there is no matured data-centre load cohort yet**. We therefore cannot compute a historical "% energised" rate the way v0.1 did. Instead this filter does two things, and the first is a gift: **PJM performs and publishes the announced-vs-deliverable deflation itself, with a documented, reproducible method.**

## What PJM publishes (see dc_funnel.csv) - all primary

PJM reports three curves for large-load demand (Requests Summary, slides 7-8):
- **Submitted (requested):** ~60 GW for 2030, rising to ~115 GW by 2046.
- **Proposed (PJM-accepted, preliminary):** ~38 GW for 2030, rising to ~88 GW by 2046.
- **Firm only (ESO/CC-backed - the subset that counts toward capacity/RPM):** ~61 GW at the 2046 plateau, i.e. ~53% of requested at the long end.

PJM's own data-centre-specific statement (slide 5): it supports **"up to ~30 GW of data-centre growth 2025-2030,"** noting PJM is ~40% of US data centres in 2025 and that it cross-checked FT, Deloitte, BCG, McKinsey, BNEF rather than relying on one source.

## The documented haircut mechanics (Implementation doc - reproducible)

PJM's vetting is explicit, which is what makes this reproducible rather than a guess:
- **Firmness filter:** only projects with an Electric Service Obligation (ESO) or Construction Commitment (CC) are "Firm" and allowed to impact RPM/capacity; everything else is "Non-Firm" (Requests Summary slide 4).
- **Default 50% probability** applied to non-firm projects coming online in 3-8 years absent an EDC/LSE-supplied factor; 8+ years is extrapolation.
- **70% utilization** rate imposed per data centre unless otherwise supported.
- **70% capacity-to-demand** factor (the forecast runs on demand, not nameplate capacity).
- **Minimum 36-month ramp** to full demand.
- **Worked example (Implementation doc p4):** 2,600 MW requested capacity -> 1,800 after probability (x~69%) -> **1,260 MW demand (x70%)** = **~48% of requested capacity survives** to the demand figure that enters the forecast. AEP's submission (slide 14) was de-rated by >50%.

## The deflation, stated

- **PJM has already cut the 2030 large-load ask from ~60 GW (submitted) to ~38 GW (accepted)** before construction - and only the **Firm** subset (ESO/CC-backed, roughly half) is allowed to count toward capacity.
- That ~38 GW accepted is still the **optimistic** end: it is forecast capacity, not energised capacity. With no matured load cohort, the energised rate is bracketed by the **generation-queue analog ~20-22%** (lower rail, labelled a proxy).
- Read the **$850B announced-lease** headline against this: PJM's own primary vetting implies roughly **half** the announced large-load ask survives to the forecast, and historical interconnection completion is far lower again. Announced is a scenario, not a baseline.

## Two-rail bracket for the deliverable rate

- **Upper rail (PJM accepted):** ~38/60 = ~63% of 2030 submitted survives vetting into the forecast (less further out: ~88/115 = ~77% by 2046 on the proposed line, but Firm-only is ~53%).
- **Lower rail (generation-queue analog):** ~20-22% reach commercial operation (v0.1 / LBNL Queued Up) - a proxy for energisation, clearly labelled.
- The band and the gap are the finding, not a crash call.

## Supporting factors (now primary-confirmed)

- **De-dup / phantom:** developers file identical requests across utility queues (Wood Mackenzie); PJM's stated aim is to have LSEs and states cut duplicative submittals.
- **Viability gate hardening:** FERC order 18 Dec 2025 + PJM CIFP; the Expedited Interconnection Track (eff. ~Aug 2026) requires a **$15,000/MW refundable readiness deposit + 100% of network-upgrade cost + state siting support** - so future firm cohorts should complete above a naive historical floor (name this assumption).
- **Sanity rail (not a demand estimate):** PJM capacity prices $28.92 -> $269.92 -> $329.17/MW-day (held by a cap) = ~10x (IEEFA) - coarse confirmation the inflation is material to ratepayers.

## Scope discipline (unchanged)

Not a crash call; a band plus a named load-bearing assumption (the announced-vs-deliverable gap; cohort comparability). Deflated demand is *avoided* (never built) or *stranded* (built, idled), not "efficiency saved."

## Final-report lock (2026 LTLF, posted 14 Jan 2026 - VERIFIED against the official report)

The official 2026 Long-Term Load Forecast Report confirms the deflation and the method first-hand:
- The 2026 LTLF is **lower than the 2025 LTLF in the near term through 2032** specifically because of EV, economic, and **large-load** adjustments, and PJM states the firm (ESO/CC) vs non-firm distinction **"has brought large load adjustments down in the near-term forecast years."**
- Specific revisions vs the 2025 report: **3rd IA 2026 -2,564 MW (-1.6%); RPM Auction 2028 -4,414 MW (-2.6%); RTEP 2031 -1,630 MW (-0.8%).**
- Zones explicitly adjusted for data-centre load: AEP, ATSI, APS, BGE, COMED, DAYTON, DLCO, JCPL, METED, PECO, PEPCO, PL (plus DOM with voltage optimization, PS with port electrification).
- So the ~38 GW "Proposed" (24 Nov 2025 preliminary) is the best published single accepted figure; the **exact final accepted large-load GW by year lives in Tables B-9 / B-9b**, which the report says are now Excel-only. That spreadsheet is the only remaining last-mile precision lock; the headline direction, the method, and the revision magnitudes are now primary-final.

## ERCOT cross-region rail (v2 - PRIMARY-verified 2026-06-25)

The second region. ERCOT is the cleanest cross-region check because, unlike PJM, it (a) had almost no barrier to entry before PGRR115, so its queue is maximally padded, and (b) publishes a *realized* (observed, not assumed) per-site de-rate. Figures locked in `ercot_funnel.csv`; all multi-sourced.

- **Requested:** ~226 GW large-load interconnection queue (Dec 2025), ~70-77% data centres, up from ~63 GW a year earlier (ERCOT System Planning Update Dec 2025, via Belfer Center; Utility Dive cites ~233 GW at the 9 Dec 2025 board). ERCOT itself: most "will not materialize."
- **ERCOT's own realized de-rate = 49.8%** of requested MW (average per-site peak consumption for sites with 2022-2024 in-service dates; ERCOT Long-Term Load Forecast 2025, applied to non-crypto data-centre additions). A *separate* ERCOT figure via WECC Fig 2.2: only 58-78% of requested transmission service is used on peak within a year (ramp/utilization).
- **Energized to date:** 5,302 MW (~5.3 GW) approved-and-observed-energized since 2022, as of 18 Nov 2025 = ~2% of ERCOT large-load tracking (ERCOT Large Load Interconnection Process Q&A, 24 Dec 2025). Timing-limited (the surge is too young), NOT a completion rate.
- **Credible 2030 scenario:** ~35 GW data-centre load by 2030 (Aurora Energy Research, ERCOT-commissioned resource-adequacy study) = ~15% of the requested queue, ~10x today's operational.
- **The forecast gate (ERCOT analog of PJM's Firm/ESO-CC):** PGRR115 / NPRR1234, effective 15 Dec 2025; approval-to-energize requires executing all agreements + notice to proceed + financial obligations (ERCOT Planning Guide 9.5). Going forward, only executed-agreement loads enter the large-load forecast. SB6 adds upfront study fees + duplicate-request disclosure; PUCT rulemaking due Dec 2026.

### The cross-region finding (the v2 contribution)

Two independent grid operators, different methods, same conclusion: the requested queue is a scenario, not a baseline, and roughly **half** survives the first credible screen.

- PJM applies a *forward* de-rate: 2,600 MW requested -> 1,260 MW demand = **~48%** survives into the forecast (probability ~0.69 x utilization 0.70).
- ERCOT measures a *realized* de-rate: actual per-site peak = **49.8%** of requested MW.

**Honest caveat (do not overclaim the numeric match):** these two ~50% figures are *constructed differently* - PJM's bundles a completion-probability factor; ERCOT's is conditional on the project having been built (pure peak-vs-requested utilization). So ERCOT's 49.8% is independent empirical support for the *order of magnitude* of PJM's applied haircut, not a like-for-like identity. The robust, defensible statement is structural: both operators (i) find requested >> deliverable, (ii) haircut by ~half at the first credible step, and (iii) now gate the forecast on an executed agreement. State the structure; present the two numbers as similar-in-magnitude, differently-built.

## NEXT STEP (status 2026-06-25)

DONE this session: ERCOT rail locked (`ercot_funnel.csv`); v2 paper drafted + rendered; index.html DC-load view + build.py consts; README + .zenodo.json; paper zenodo metadata for `--newversion`. Optional precision still open: pull exact PJM B-9/B-9b GW-by-year from the Excel supplement for a single headline figure. Mint = Noel's terminal step (DOI question flagged: repo cites 20559430 [interactive], resume note says --newversion 20706509 [paper] - confirm which record before minting).

## Sources

- PJM, *Load Adjustment Request Implementation* (1 Jul 2025) - mechanics, the 2,600->1,260 worked example.
- PJM LAS, *Load Adjustment Requests Summary for 2026 Load Forecast - Preliminary* (24 Nov 2025) - submitted/proposed/firm curves, the ~30 GW DC statement, the 50%/70%/36-month rules.
- PJM, *2026 Long-Term Load Forecast Report* (Jan 2026) - final accepted figures (pending lock).
- Contingent v0.1 (DOI 10.5281/zenodo.20706509) - generation-queue completion proxy.
- Framing: Maryland OPC, Wood Mackenzie, IEEFA, FERC order 18 Dec 2025.
- ERCOT rail: ERCOT System Planning and Weatherization Update (Dec 2025); ERCOT Large Load Interconnection Process Q&A (24 Dec 2025); ERCOT Long-Term Load Forecast 2025 (the 49.8% per-site figure); ERCOT/NPRR1234/PGRR115 market notices (forecast gate, eff. 15 Dec 2025); Aurora Energy Research RA study for ERCOT (35 GW 2030 scenario); WECC, Assessment of Large Load Interconnection Risks (2025, Fig 2.2, 58-78% transmission-service-used-on-peak); Belfer Center, Data Centers and Large-Scale Electric Growth: Virginia and Texas (2026); Utility Dive / Latitude Media (queue-growth reporting, citing ERCOT board figures). Texas SB6 (2025).
