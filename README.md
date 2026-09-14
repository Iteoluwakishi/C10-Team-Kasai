Absolutely. Here is a **shortened GitHub README under 6,000 characters**, while retaining the important project, technical, evaluation, notebook, and limitation information.

```markdown
# C10-Team-Kasai

> An ethically guided, RAG-powered Small Language Model (SLM) delivering accurate, transparent, and plain-language legal answers regarding Nigerian tax laws for SMEs and individuals.

# Kasai — Nigerian Tax Law Small Language Model

Kasai is a domain-adapted Small Language Model (SLM) designed to assist with **Nigerian tax-law questions and scenarios**, particularly under the tax reforms that took effect on **1 January 2026**.

The project explores whether a small open-weight model can be specialized for Nigerian tax law using **Supervised Fine-Tuning (SFT) with LoRA**, while evaluating legal AI challenges such as factual accuracy, citations, current-law recognition, repealed-law detection, reasoning, and uncertainty.

> **Research prototype — not legal advice.**  
> Kasai v0.1 is not validated for professional or production legal/tax use.

---

## 🎯 Problem

General-purpose LLMs can:

- rely on repealed legislation;
- confuse current and historical tax rules;
- provide incorrect statutory citations;
- mix Nigerian law with other jurisdictions;
- confidently answer questions when information is insufficient.

Kasai investigates whether domain adaptation can improve Nigerian tax-law alignment while providing a framework for measuring these limitations.

---

## 🧠 Approach

```text
Nigerian Tax-Law Corpus
        ↓
Data Preprocessing
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

### Model & Training

- **Base model:** Google Gemma 3 4B Instruct
- **Method:** LoRA / SFT
- **Training records:** 96
- **Epochs:** 3
- **Learning rate:** `2e-4`
- **Batch size:** 1
- **Gradient accumulation:** 8
- **Trainable parameters:** ~29.8M
- **Quantization:** 4-bit NF4
- **Training hardware:** NVIDIA Tesla T4

---

## 📚 Legal Domain

The initial corpus covers:

- Nigeria Tax Act (NTA)
- Nigeria Tax Administration Act (NTAA)
- Nigeria Revenue Service Establishment Act (NRSEA)
- Joint Revenue Board Establishment Act (JRBA)
- Nigeria Revenue Service circulars, FAQs and notices
- Selected repealed legislation for negative/repeal testing

Key areas include:

- Company Income Tax
- VAT
- PAYE
- Personal Income Tax
- SME taxation
- Withholding Tax
- Tax administration
- Current vs. repealed legislation

---

## 🧪 Evaluation

Kasai uses a dedicated legal benchmark covering:

| Category | Focus |
|---|---|
| Factual Accuracy | Correct tax-law facts |
| Legal Interpretation | Interpretation of provisions |
| Legal Reasoning | Applying interacting provisions |
| Citation Accuracy | Correct statutory references |
| Citation Completeness | Supporting provisions |
| Current-Law Recognition | Identifying legislation in force |
| Repealed-Law Detection | Rejecting superseded law |
| Temporal Reasoning | Distinguishing rules by period |
| Scenario/Application | Applying law to scenarios |
| Abstention | Recognizing insufficient information |

### Repealed-Law Testing

A key Kasai feature is testing whether the model can identify questions based on **repealed legislation** rather than blindly applying outdated rules.

```text
Question
   ↓
Is the referenced law current?
   ├── Yes → Apply current law
   └── No  → Identify/reject repealed framework
```

---

## 📊 v0.1 Results

Kasai v0.1 was evaluated using a **12-question pilot benchmark** and compared against the untuned Gemma 3 4B model.

The fine-tuned model demonstrated improved **Nigerian tax-domain alignment**, but the evaluation also revealed limitations in:

- statutory citation accuracy;
- tax calculations;
- legal reasoning;
- repealed-law detection;
- abstention;
- generation consistency.

Therefore, Kasai v0.1 is a **research prototype**, not a production-ready tax-law system.

> **Domain alignment ≠ legal reliability.**

---

## 🚀 Running Kasai

The repository includes the complete Google Colab notebook:

**`Kasai_legal_SLM.ipynb`**

The notebook provides an end-to-end workflow:

```text
Environment Setup
↓
Hugging Face Authentication
↓
Gemma 3 4B Loading
↓
Dataset Preparation & Validation
↓
LoRA Configuration
↓
SFT Training
↓
Adapter Saving
↓
Inference
↓
Evaluation
↓
Base vs. Kasai Comparison
↓
Submission Packaging
```

### Requirements

The notebook was tested using:

- Google Colab
- CUDA GPU
- NVIDIA Tesla T4 (~14.6 GB VRAM)
- Hugging Face authentication

The model is loaded in 4-bit NF4 quantization to reduce memory requirements.

The Hugging Face token should be stored in Colab Secrets as:

```text
HF_TOKEN
```

### Kasai Adapter

Kasai v0.1 is distributed as a **LoRA adapter** and must be loaded on top of:

```text
google/gemma-3-4b-it
        +
Kasai v0.1 Adapter
        ↓
Kasai v0.1
```

The notebook also generates:

```text
kasai_sft_v0.1/
evaluation_dataset.jsonl
kasai_sft_v0.1_test_results.json
kasai_v0.1_full_evaluation.json
Kasai_v0.1_submission.zip
```

---

## 🔮 Future Work

Future versions will focus on:

- Larger expert-reviewed datasets
- Retrieval-Augmented Generation (RAG)
- Version-aware legal retrieval
- Citation verification
- Stronger repealed-law detection
- Improved legal reasoning
- Better abstention
- Human expert evaluation
- Automated regression testing
- RAG + SLM architecture
- Resource-efficient deployment

```text
User Question
      ↓
Legal Retrieval
      ↓
Current-Law / Repeal Verification
      ↓
Kasai
      ↓
Answer + Citations
```

---

## 🛡️ Responsible AI

Kasai is guided by:

**Accuracy · Reliability · Explainability · Transparency · Fairness · Privacy · Inclusivity · Safety**

Kasai should not replace qualified tax professionals or authoritative legal sources.

Generated answers should always be verified against the latest Nigerian legislation, regulations, and official guidance.

---

## 📄 Disclaimer

**Kasai v0.1 is an experimental research project and is not a legal or tax advisory service.**

It must not be relied upon for tax filing, compliance decisions, litigation, financial decisions, or professional legal/tax advice.

---

## 📜 License

Add the project's chosen license here.

The project license does not override the licensing terms of the underlying Gemma model or source materials.
```
