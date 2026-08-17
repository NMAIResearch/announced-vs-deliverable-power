#!/usr/bin/env python3
"""
Rebuild index.html by embedding the published aggregate CSVs into it.

  funnel.csv      -> const FUNNEL   (the completion funnel, 2010-2017 cohort)
  cohorts.csv     -> const COHORTS  (realized completion by submitted cohort)
  dc_funnel.csv   -> const DCPJM    (load side: PJM large-load funnel)
  ercot_funnel.csv-> const DCERCOT  (load side: ERCOT cross-region rail)

No raw PJM data is bundled (it is redistribution-restricted); only the
published derived aggregates. Edit a CSV, run `python3 build.py`, commit.

Pure standard library, no dependencies.
"""
import re
import sys
import pathlib

HERE = pathlib.Path(__file__).parent
HTML = HERE / "index.html"
BLOCKS = [("FUNNEL", HERE / "funnel.csv"), ("COHORTS", HERE / "cohorts.csv"),
          ("DCPJM", HERE / "dc_funnel.csv"), ("DCERCOT", HERE / "ercot_funnel.csv")]


def main() -> int:
    if not HTML.exists():
        print("error: run this from the folder containing index.html")
        return 1
    html = HTML.read_text(encoding="utf-8")
    for var, csv_path in BLOCKS:
        if not csv_path.exists():
            print(f"error: missing {csv_path.name}")
            return 1
        csv_text = csv_path.read_text(encoding="utf-8").strip()
        if "`" in csv_text:
            print(f"error: {csv_path.name} contains a backtick")
            return 1
        pat = re.compile(r"(const " + var + r" = `)(.*?)(`;)", re.DOTALL)
        if not pat.search(html):
            print(f"error: could not find the `const {var} = ` ... `;` block")
            return 1
        html = pat.sub(lambda m: m.group(1) + csv_text + m.group(3), html)
        print(f"embedded {csv_text.count(chr(10))} data rows into const {var}")
    HTML.write_text(html, encoding="utf-8")
    print("done. next: commit index.html (and the CSVs) and push.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
