# Data in the public repository

`demo/loan_demo.csv` contains 12 entirely artificial records created for the Python audit. IDs begin with `DEMO-`; demographic labels are explicitly artificial. These are not sampled or perturbed customer rows.

`expected/demo-audit.json` is the deterministic expected audit result for that fixture. The artificial default rate is not a result on the teaching dataset and is not model performance.

The real course CSV and embedded PBIX records remain in ignored local storage. Aggregate statistics are under `analysis/`, with source checksums and metric definitions. The public audit runs without access to the course material.
