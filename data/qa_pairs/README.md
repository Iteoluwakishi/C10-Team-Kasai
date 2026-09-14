# Q&A Dataset — Combined (78 rows, hand-generated from your 6 documents)

Everything from both rounds, merged into one set. All from the documents
you uploaded — no gaps, no other sections outstanding on my end for this
pass.

## What's in here

- **`candidate_questions.jsonl`** (78 rows)
- **`candidate_answers.jsonl`** (78 rows)
- **`training_candidates.jsonl`** (78 rows) — instruction-tuning format, unreviewed
- **`source_provisions.json`** (35 provisions) — every provision traced to
  its exact Act/section, so you can audit or extend from here

## Coverage

**35 source provisions** — 29 current-law, 6 repealed/superseded:

| Act | Provisions covered |
|---|---|
| Nigeria Tax Act (NTA) | VAT rate & rules (charge, exempt & zero-rated supplies), CIT rates, individual income tax bands, capital gains treatment, development levy, mining royalty, stamp duty rates, fossil fuel surcharge, income tax exemptions |
| Nigeria Tax Administration Act (NTAA) | TIN registration, company/PAYE filing deadlines, and 10 separate offence/penalty provisions (failure to register, file, keep books, grant tech access, use fiscalisation, deduct/remit tax, false refund claims, royalty default) |
| Nigeria Revenue Service Act (NRSEA) | The Service's functions |
| Joint Revenue Board Act (JRBA) | Board's functions, Office of the Tax Ombud |
| Withholding Regulations 2024 | WHT rates by transaction type |
| Repealed Acts (CITA, VAT Act, CGTA, PITA, old FIRS Act, old Joint Tax Board) | 6 current-vs-repealed contrast pairs |

**By type:** 28 basic · 16 contextual · 16 legal_interpretation · 12 scenario · 6 current_vs_repealed
**By difficulty:** 23 easy · 25 medium · 23 hard · 7 expert

## What changed from the first batch

The first batch (47 rows) covered headline rates, registration, and the
new institutions. This round dug into sections I hadn't touched yet:

- **NTA's other tax bases** — stamp duty (with actual ad valorem rates per
  instrument type), the 4% development levy, mining royalty, the 5% fossil
  fuel surcharge, and the VAT exempt vs. zero-rated distinction (these are
  legally different even though both mean "no VAT charged" — worth a
  careful look from your legal lead, since it affects input-tax-credit
  eligibility downstream).
- **NTAA's offence catalogue (§100-123)** — ten separate penalty
  provisions with exact naira figures and percentages, which is exactly
  the kind of precise, easy-to-get-wrong detail a domain-specific model
  should outperform a general-purpose one on.

## Two rows flagged for extra scrutiny in review

- **`q_exempt_2`** — asks whether a trade union's separate trading profit
  is tax-exempt. I marked this `confidence: medium` because the answer
  turns on how "carried on by the trade union" gets applied to a specific
  fact pattern — a judgment call better made by your legal/domain lead
  than inferred from the statute text alone.
- **`q_vatzero_2`** — explains the exempt-vs-zero-rated distinction. I'm
  confident in the legal difference itself, but flagged it as a good one
  for the review pass to double check the input-tax-credit implication I
  mentioned, which the source text doesn't spell out explicitly.

## Still not exhaustive

This is 35 provisions out of ~1,000 pages, focused on what's most likely
to come up in real tax-compliance questions (rates, deadlines, penalties,
exemptions). Full coverage of every section — every petroleum/hydrocarbon
provision, every economic development incentive clause, every offence in
NTAA's Part II (petroleum-specific offences), etc. — is still ahead.
Tell me which areas to prioritize next, or hand this off to the scripted
pipeline for exhaustive unattended coverage once the corpus is structured.

## Before this touches fine-tuning

Same rule as before: every row has `"reviewed": false, "approved": null`
in `training_candidates.jsonl`. Nothing here should go into an actual
training run until your legal/domain lead has been through it.
