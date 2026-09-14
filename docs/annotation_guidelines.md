# Kasai annotation guidelines

How to create, fill, and review dataset examples. The machine-readable contract
is [`annotation/dataset_schema.json`](../annotation/dataset_schema.json); every
record in every `.jsonl` dataset file must validate against it
(`python src/annotation_pipeline/03_validate_dataset.py <file>`).

## Core principles

1. **Every example traces to a provision.** `provenance.chunk_id` must point at
   a real chunk in `data/processed/`. No source → the example does not exist.
2. **LLM output is never automatically data.** Generated questions/answers enter
   with `review.status: "pending"` and only legal reviewers can set
   `approved`. Only approved records reach train/validation/test.
3. **Current and repealed law never mix silently.** `legal_status` is mandatory;
   `repealed`/`superseded` examples go to the negative benchmark, not training.

## Field reference

| Field | Meaning | Filled by |
|---|---|---|
| `id` | `PREFIX_NNN`, unique across the dataset (e.g. `VAT_001`, `NRSEA_014`). Assigned by the pipeline — don't hand-pick. | pipeline |
| `instruction` | The user-facing question/task. Natural language, self-contained, unambiguous (see "Writing questions"). | annotator |
| `context` | Verbatim provision text from the corpus chunk, trimmed to the relevant part. Don't paraphrase — it must stay quotable law. | pipeline + annotator trims |
| `response` | The grounded answer (see "Writing answers"). | annotator |
| `source` | Human-readable title of the law/document. | pipeline |
| `law` | Short identifier: `NRSEA`, `JRBA`, `NTA`, `NTAA`, `CITA`, `PITA`, `VATA`, `NRS_CIRCULAR_2026_01`, `NRS_FAQ`, … | pipeline |
| `section` / `subsection` | Where in the law: `"12"`, `"4(2)"`; circular heading `"6.1"`; FAQ topic. | pipeline |
| `tax_domain` | One of the schema's enum values. **Provisional until Cecilia's `taxonomy.json` lands** — then the enum is regenerated from it. | annotator |
| `topic` | Topic within the domain (`Registration`, `Tax Rate`, `Filing`). Use Cecilia's taxonomy labels once published. | annotator |
| `question_type` | See below. | annotator |
| `difficulty` | `easy` (single fact) / `medium` (fact + who/when) / `hard` (multiple provisions or conditions) / `expert` (multi-source reasoning, edge cases). | annotator |
| `legal_status` | `current` / `amended` / `repealed` / `superseded` / `transitional`. Comes from the corpus metadata; a reviewer may correct it. | pipeline, reviewer verifies |
| `effective_date` | ISO date the provision took effect (`2025-06-26`), empty if unknown. | pipeline |
| `replacement_legislation` | For repealed law: what replaced it (`Nigeria Tax Act 2025`). | pipeline/annotator |
| `provenance` | `chunk_id`, `document_id`, `source_file`, `page`, `source_url`. Never edit by hand. | pipeline |
| `review` | `status` + `reviewer` + `notes`. Only KeshTech/Cecilia set `approved`/`rejected`/`revise`. | reviewers |

### `question_type` values

- `definition` — what something is ("What is the Development Levy?")
- `rate` — a percentage/amount ("What is the VAT rate?")
- `threshold` — a limit that triggers an obligation
- `calculation` — compute something from given figures
- `compliance` — obligations, deadlines, filings
- `exemption` — what is excluded/zero-rated/exempt
- `procedure` — how a process works (registration, refunds, appeals)
- `interpretation` — which provision governs; what a provision means
- `scenario` — apply the law to a described fact pattern
- `comparison` — old vs new law, or two regimes side by side

## Writing questions

- Self-contained: the model won't see our metadata. Bad: *"What does this
  section say?"* Good: *"Which body appoints the Executive Chairman of the
  Nigeria Revenue Service?"*
- Unambiguous: *"What tax does a company pay?"* is too broad → *"What tax
  obligation applies to a Nigerian company with taxable profits under the
  current tax framework?"*
- Vary phrasing per provision: basic / contextual / scenario / interpretation
  variants of the same rule teach the concept, not the wording.

## Writing answers

- Derivable from `context` alone — if you needed outside knowledge, the context
  is wrong or the example belongs elsewhere.
- Name the basis: *"Under section 4 of the NRS (Establishment) Act, 2025, …"*
- For guidance sources (circulars/FAQs), the answer must reflect that circulars
  are administrative guidance, not law, when the distinction matters.
- Negative examples (repealed law): the answer must explicitly say the old law
  is repealed and name the replacement:
  *"No — CITA has been repealed. Company income tax is now governed by the
  Nigeria Tax Act 2025 (effective 1 January 2026)."*

## Review workflow (KeshTech / Cecilia)

For each `pending` record check, in order:
1. Question legally valid, relevant, unambiguous?
2. Does the cited provision actually answer it? (anti-hallucination check)
3. Answer accurate, complete, correct terminology?
4. `legal_status` correct? Current/repealed not confused?
5. High-risk content (rates, thresholds, deadlines, penalties, exemptions,
   transitional provisions, effective dates) gets extra scrutiny.

Then set `review.status` to `approved`, `rejected`, or `revise` (with
`review.notes` explaining what to change), and put your name in
`review.reviewer`.

## Pipeline usage

```
# 1. provisions catalog from the processed corpus (all laws, incl. repealed)
python src/annotation_pipeline/01_extract_provisions.py

# 2. merge Q&A drafts with provisions into schema-conformant records
python src/annotation_pipeline/02_make_candidates.py data/annotation/drafts/<your_drafts>.jsonl

# 3. validate any dataset file against the schema
python src/annotation_pipeline/03_validate_dataset.py data/annotation/candidates.jsonl

# 4. export only approved records for the dataset splits
python src/annotation_pipeline/04_export_approved.py
```

Draft format for step 2 (one JSON per line — this is what Kishi produces):

```json
{"chunk_id": "nrsea_2025#004", "instruction": "…", "response": "…",
 "tax_domain": "revenue_administration", "topic": "Functions of the NRS",
 "question_type": "definition", "difficulty": "easy"}
```

Everything else (context, source, law, section, legal_status, effective_date,
provenance, id) is filled automatically from the provisions catalog.
