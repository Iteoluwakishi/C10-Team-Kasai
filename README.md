# Kasai — Nigerian Tax Law Small Language Model

> An ethically guided Small Language Model (SLM) for accurate, transparent, and plain-language answers to Nigerian tax-law questions.

Kasai is a domain-adapted SLM designed to assist with Nigerian tax-law questions and scenarios, particularly under the tax reforms effective **1 January 2026**.

The project investigates whether a small open-weight model can be specialized for Nigerian tax law using **Supervised Fine-Tuning (SFT) with LoRA**, while evaluating factual accuracy, legal reasoning, citation quality, current-law recognition, repealed-law detection, and uncertainty.

> **Research prototype — not legal advice.**

## Problem

General-purpose LLMs may:

- Rely on repealed legislation
- Confuse current and historical tax rules
- Produce incorrect statutory citations
- Mix Nigerian law with other jurisdictions
- Answer confidently when information is insufficient

Kasai focuses on reducing these risks through domain adaptation and legal-specific evaluation.

## Approach

```text
Nigerian Tax-Law Corpus
        ↓
Preprocessing & Legal-Aware Chunking
        ↓
SFT Dataset
        ↓
Gemma 3 4B Instruct
        ↓
LoRA Fine-Tuning
        ↓
Kasai v0.1
        ↓
Legal Evaluation
```

Future architecture:

```text
User Question
     ↓
Legal Retrieval
     ↓
Current-Law / Repeal Verification
     ↓
Kasai SLM
     ↓
Citation Verification
     ↓
Answer + Sources
```

## Legal Domain

Primary sources include:

- Nigeria Tax Act (NTA)
- Nigeria Tax Administration Act (NTAA)
- Nigeria Revenue Service Establishment Act (NRSEA)
- Joint Revenue Board Establishment Act (JRBA)
- NRS circulars, FAQs, and notices
- Selected repealed legislation for negative testing

Focus areas include **CIT, VAT, PAYE, PIT, SME taxation, WHT, tax administration, compliance, and current vs. repealed law**.

## Dataset

The corpus follows:

```text
Legal Documents
 → PDF Inspection
 → Text Extraction/OCR
 → Metadata Classification
 → Text Cleaning
 → Legal Structure Parsing
 → Legal-Aware Chunking
 → Dataset Construction
 → Validation
 → Train / Validation / Test Sets
```

The dataset emphasizes temporal reasoning and distinguishing current legislation from historical/repealed law.

## Training

Kasai v0.1 uses **SFT with LoRA**, rather than training a model from scratch.

| Configuration | Value |
|---|---|
| Base Model | Google Gemma 3 4B Instruct |
| Training Records | 96 |
| Epochs | 3 |
| Learning Rate | 2e-4 |
| Batch Size | 1 |
| Gradient Accumulation | 8 |
| Trainable Parameters | ~29.8M |
| Quantization | 4-bit NF4 |
| Precision | BF16 |
| GPU | Tesla T4 |

LoRA reduces the number of parameters that must be updated during fine-tuning.

## Evaluation

Kasai uses a dedicated legal benchmark covering:

- Factual accuracy
- Legal interpretation
- Legal reasoning
- Citation accuracy and completeness
- Current-law recognition
- Repealed-law detection
- Temporal reasoning
- Scenario/application
- Abstention

The same benchmark is used to compare the **base Gemma 3 4B model** against **Kasai SFT v0.1**.

### Repealed-Law Benchmark

A key Kasai component is testing whether the model can recognize outdated legislation and identify the applicable current framework rather than confidently relying on repealed law.

## Kasai v0.1 Results

A 12-question pilot benchmark showed improved Nigerian tax-domain alignment after SFT.

However, Kasai v0.1 still showed weaknesses in:

- Statutory citation accuracy
- Tax calculations
- Legal reasoning
- Repealed-law detection
- Abstention
- Generation consistency

These results demonstrate that domain fine-tuning alone does not guarantee legal correctness.

## Reproduction

Experimental environment:

- Google Colab
- Python 3.13
- PyTorch 2.11.0+cu128
- Transformers 4.57.3
- bitsandbytes 0.50.2
- CUDA 12.8
- Tesla T4
- 4-bit NF4 / BF16

General workflow:

```text
Environment Setup
 → Hugging Face Authentication
 → Gemma Loading
 → Dataset Validation
 → LoRA Configuration
 → SFT
 → Adapter Saving
 → Inference
 → Evaluation
 → Base vs. Kasai Comparison
```

Kasai v0.1 is distributed as a **LoRA adapter** on top of `google/gemma-3-4b-it`.

Never commit Hugging Face tokens or credentials to the repository.

## Artifacts

Key research artifacts include:

```text
evaluation_dataset.jsonl
repealed_law_benchmark.jsonl
evaluation_metrics.md
kasai_sft_v0.1/
kasai_v0.1_full_evaluation.json
kasai_v0.1_test_results.json
Kasai_v0.1_submission.zip
Kasai_legal_SLM.ipynb
```

## Limitations

Kasai remains an experimental research system. Limitations include:

- Limited dataset size and coverage
- Potential errors in source extraction
- Changing Nigerian legislation
- Citation hallucinations
- Tax calculation errors
- Imperfect legal reasoning
- Imperfect repeal detection
- Limited benchmark size
- No guarantee of professional legal reliability

## Future Work

- Expert-reviewed training data
- Retrieval-Augmented Generation (RAG)
- Version-aware legal retrieval
- Citation verification
- Stronger repeal detection
- Improved reasoning and abstention
- Human expert evaluation
- Automated regression testing
- RAG + SLM architecture
- Resource-efficient deployment

## Responsible AI

Kasai is guided by:

**Accuracy · Reliability · Explainability · Transparency · Fairness · Privacy · Inclusivity · Safety**

The system should prioritize current legislation, communicate uncertainty, ground legal claims in authoritative sources, and encourage verification for consequential decisions.

## Disclaimer

Kasai v0.1 is an **experimental research prototype** and is not a legal or tax advisory service. It should not be relied upon for tax filing, compliance, litigation, financial decisions, or professional legal/tax advice.

## License

The project license will be specified separately. Project licensing does not override the licenses of Gemma or the underlying legal/source materials.

# Appendix

### A. Contributors

**Team Members**

- **Akorede Aboaba**
- **Iteoluwakishi Adeniran**
- **Abdulmalik Sulaimon**
- **Keshinro Mus'ab Moyosore**
- **Ceclia Olabode**

**Mentors**

- **David Taiwo**

### B. Research Artifacts

Dataset, preprocessing pipeline, SFT configuration, evaluation benchmarks, model outputs, comparison reports, and reproduction notebooks.

### C. Evaluation Metrics

Legal Correctness · Factual Accuracy · Citation Accuracy · Current-Law Accuracy · Reasoning · Repealed-Law Detection · Abstention

### D. Research Position

Kasai is a research project exploring **domain adaptation of small language models for Nigerian tax-law applications**, with particular emphasis on legal accuracy, temporal awareness, citation reliability, and responsible AI.
