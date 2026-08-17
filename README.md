# Announced vs. Deliverable AI Power Demand (interactive)

An interactive front-end to *Announced vs. Deliverable AI Power Demand*. The thesis is simple: *announced capacity is a scenario, not a baseline*, and the tool deflates it on **both sides of the meter**: the **supply** side (a realized announced-to-in-service completion anchor from the PJM generation queue) and the **load** side (how much announced data-centre demand survives the grid operators' own screens, across PJM and ERCOT).

**Live tool:** https://nmairesearch.github.io/announced-vs-deliverable-power/
**Canonical record (concept DOI, auto-resolves to latest):** [DOI 10.5281/zenodo.20559430](https://doi.org/10.5281/zenodo.20559430)
**Version 1 record (2026-08):** [DOI 10.5281/zenodo.21971645](https://doi.org/10.5281/zenodo.21971645)
**Author:** NM AI Research · ORCID [0009-0003-4213-7769](https://orcid.org/0009-0003-4213-7769) · Licence CC BY 4.0

## What it does

Three views, switched at the top:

- **Deflation calculator.** Enter an announced capacity (GW) and move three sliders: de-duplication (r1), viability survival (r2, entered to signed agreement), and build rate (r3, agreement to in service). A live waterfall shows how much survives each stage and what is finally deliverable. Defaults are the PJM mature-cohort measured base rate (r1 ≈ 0.85, r2 ≈ 0.39, r3 ≈ 0.58, giving roughly one announced MW in five built); the sliders are for sensitivity, not invention. "Reset" returns to the measured anchor.
- **PJM supply evidence.** The published completion funnel (2010–2017 cohort, 204 GW entered) and realized completion by submitted cohort: the empirical base rate behind the calculator's defaults.
- **Data-centre load.** The demand side. PJM's published large-load funnel (submitted ≈60 GW, accepted ≈38 GW, firm ≈32 GW for 2030) beside ERCOT's (requested ≈226 GW; realized per-site de-rate 49.8%; ≈5.3 GW energized to date) and the two-rail energisation bracket (≈20% floor to ≈48–63% ceiling). The operators perform the deflation; the tool packages it cross-region and brackets it.

## Important: no raw PJM data here

The **supply-side** PJM serial-queue export carries a redistribution restriction, so this repository bundles **only the published derived aggregates** (`funnel.csv`, `cohorts.csv`); the full method (`reproduce.py`) reads a locally-obtained PJM export and is reproducible only by someone who has independently obtained PJM access. The **load-side** aggregates (`dc_funnel.csv`, `ercot_funnel.csv`) are different: they are transcribed from public PJM and ERCOT documents (the LAS large-load summary, the 2026 LTLF, ERCOT's Large Load Interconnection Process Q&A and LTLF), so they carry no such restriction and are reproducible from the cited filings.

## Files

- `index.html`: the interactive tool, self-contained (no dependencies, no server needed).
- `funnel.csv`, `cohorts.csv`: the supply-side published aggregates.
- `dc_funnel.csv`, `ercot_funnel.csv`: the load-side aggregates (PJM + ERCOT).
- `paper_v1.md`, `paper_v1.html`, `paper_v1.pdf`: the v1 working paper and its rendered house-style versions.
- `claims.json`: the machine-readable claims passport (every headline figure with source, motive-tier, reproducibility tier, uncertainty, and the misreads to avoid).
- `check_claims.py`: verifies `claims.json` against the CSVs and prose so the passport cannot drift (pure standard library).
- `reproduce.py`: regenerates every supply-side table from the primary PJM planning data.
- `build.py`: regenerates `index.html` by embedding the CSVs (pure standard library).

## Guardrails

On the supply side, the mature 2010–2017 cohort is *generic historical generation* used as a completion base rate, not capacity announced to serve AI: transferring that rate to the AI cohort is the named load-bearing assumption (cohort comparability), which holds where the binding constraint is the shared grid. On the load side, the operators perform the deflation themselves; the tool packages and brackets it, and the two ≈50% first-screen figures (PJM applied, ERCOT realized) are constructed differently, so the cross-region claim is structural rather than a numeric identity. "Built" counts only In Service (conservative). Every output is a band; treat any announced figure as a scenario, not a baseline.

## Conflict of interest and disclosure

The research design, method, sourcing decisions and analytical judgements are the author's. Anthropic Opus 4.8-5.0 and Google Gemini 3.7 assisted with data retrieval, calculation, literature search, verification and drafting. Both assisting vendors maintain commercial relations to the AI data-centre buildout and electricity demand examined, disclosed for completeness. No third party reviewed, funded, or directed this work. Independent analysis, not investment advice.

## Licence

Creative Commons Attribution 4.0 International (CC BY 4.0).
