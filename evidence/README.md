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
| Student-named 15-page report | Nine selected original PNG screenshots, metric transcription and figure manifest | Historical dashboards, process states, result excerpts and confusion matrices |
| `1.pdf`, 16 pages | Locally retained alternate report | Additional supplied report; public figures use the student-named edition |

The `.docx` case remains an uncompleted template, whose sample images are not project evidence. The later-supplied completed PDFs provide actual work. Public figures come from the student-named report: dashboards on pages 3–4, process views on pages 7–8, result excerpts on page 9 and confusion matrices on page 11. The [figure manifest](figures/manifest.json) records source pages, image indexes, sizes and hashes. Original PDFs stay in ignored local storage.

## Portfolio additions in October 2026

The English/Traditional Chinese READMEs, methodology and interview guides, Python audit and tests, extraction script, aggregate reconciliation, public-file verifier, GitHub workflow, synthetic fixture, SVG overview and report design maps were prepared with AI assistance during portfolio organisation. They are separate from the original academic work.

Extracted DAX expressions preserve the model's text. Original M code replaces only the computer-specific source path with `CsvPath`. The separately named `Loan.portable.pq` proposes encoding and sort-key improvements. Original RMP configurations are preserved. The historical report screenshots are extracted embedded images without generative edits. Confusion counts were visually transcribed, then metrics recomputed with a separate Python audit. No native models were retrained, and no missing AUC or prediction outputs were generated.

The input hashes apply to supplied source bytes. Git attributes preserve the RapidMiner files without line-ending conversion, so the public workflow hashes match the originals. Original byte copies are also retained locally.

## Publication boundary

The author selected a public portfolio with original row-level data and PBIX kept local. The `private/` directory, all PBIX, source CSV and course documents are ignored. Only the artificial fixture is allowed as a public CSV. The verifier checks the indexed/public file list before publication and in CI.

Aggregate JSON files and selected screenshots contain category totals, model parameters and pooled confusion counts, with no borrower identifiers or individual customer records. University header artwork and assignment-template text are not included in the extracted figures. File hashes establish provenance without publishing full source documents. The portfolio does not claim that these artifacts prove a fair model, profitable lending policy or production deployment.
