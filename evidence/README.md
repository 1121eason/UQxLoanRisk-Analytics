# Evidence and contribution register

## Supplied artifacts

[`input-inventory.json`](input-inventory.json) records SHA-256 hashes, file sizes and publication status. Both PBIX inputs have the same hash. Both RapidMiner files differ and are retained separately. Windows `Zone.Identifier` files are download metadata and are excluded.

| Artifact | Public representation | Evidence boundary |
| --- | --- | --- |
| Student-named RapidMiner file | `rapidminer/loan-default-original.rmp` | Original operator configuration; no embedded model results |
| `A2.rmp` | `rapidminer/archive/loan-default-alternative.rmp` | Historical alternate configuration; not a recommended correction |
| Identical PBIX inputs | Extracted DAX, calculated columns, sanitised M and visual metadata | Code and configuration; no native UI execution |
| Loan case CSV | Aggregate audit and income summaries | Recomputed counts; raw records remain local |
| Case brief and dictionary | Paraphrased project scope and field register | Teaching context; full documents remain local |
| Rubric | Reviewed for the original task's analytical dimensions | No grade or submission-compliance conclusion |

The supplied `.docx` case is an uncompleted report template with sample visuals. Its sample images are **not** treated as the author's dashboards or analysis results. No finished report, model-results screenshot, coefficient table or trained model was supplied.

## Portfolio additions in October 2026

The English/Traditional Chinese READMEs, methodology and interview guides, Python audit and tests, extraction script, aggregate reconciliation, public-file verifier, GitHub workflow, synthetic fixture, SVG overview and report design maps were prepared with AI assistance during portfolio organisation. They are separate from the original academic work.

Extracted DAX expressions preserve the model's text. Original M code replaces only the computer-specific source path with `CsvPath`. The separately named `Loan.portable.pq` proposes encoding and sort-key improvements. Original RMP configurations are preserved; no native models were retrained and no missing performance outputs were generated.

The input hashes apply to supplied source bytes. Git attributes preserve the RapidMiner files without line-ending conversion, so the public workflow hashes match the originals. Original byte copies are also retained locally.

## Publication boundary

The author selected a public portfolio with original row-level data and PBIX kept local. The `private/` directory, all PBIX, source CSV and course documents are ignored. Only the artificial fixture is allowed as a public CSV. The verifier checks the indexed/public file list before publication and in CI.

Aggregate JSON files reveal dataset-wide statistics and category totals, with no customer identifiers or individual borrower records. File hashes establish provenance without publishing source contents. The portfolio does not claim that these artifacts prove a fair model, profitable lending policy or production deployment.
