# C10-Team-Kasai
An ethically guided, RAG-powered Small Language Model (SLM) delivering accurate, transparent, and plain-language legal answers regarding Nigerian tax laws for SMEs and individuals.




# Kasai — Nigerian Tax Law Small Language Model

Kasai is a domain-adapted Small Language Model (SLM) designed to assist with **Nigerian tax-law questions and scenarios**, with particular emphasis on the tax reforms that took effect on **1 January 2026**.

The project explores whether a relatively small open-weight language model can be adapted to a specialized legal domain using **Supervised Fine-Tuning (SFT) with LoRA**, while explicitly evaluating problems that are important in legal AI: factual accuracy, citation accuracy, current-law recognition, repealed-law detection, legal reasoning, and appropriate uncertainty.

> **Research prototype — not legal advice.**  
> Kasai v0.1 has not been validated to the standard required for professional or production legal/tax advice.

---

## 🎯 Problem

Nigeria's tax system underwent significant reform in 2025, with new legislation taking effect from **1 January 2026**.

A general-purpose LLM may:

- rely on repealed legislation;
- confuse old and current tax rules;
- provide incorrect statutory citations;
- mix Nigerian law with laws from other jurisdictions;
- confidently answer questions when the available information is insufficient.

Kasai investigates whether domain-specific training can improve a model's alignment with Nigerian tax law and whether that improvement can be measured through a dedicated evaluation framework.

---

## 🧠 Approach

Kasai v0.1 uses:

```text
Nigerian Tax-Law Corpus
        │
        ▼
Data Preprocessing
        │
        ▼
SFT Dataset
        │
        ▼
Gemma 3 4B Instruct
        │
        ▼
LoRA Fine-Tuning
        │
        ▼
Kasai v0.1
        │
        ▼
Legal Evaluation Benchmark
```

### Base Model

**Google Gemma 3 4B Instruct**

Kasai uses parameter-efficient fine-tuning rather than modifying the entire model.

### Fine-Tuning

- Method: LoRA
- Training records: **96**
- Epochs: **3**
- Learning rate: `2e-4`
- Batch size: `1`
- Gradient accumulation: `8`
- Trainable parameters: ~**29.8M**
- Quantization: 4-bit during training
- Hardware: NVIDIA Tesla T4

---

## 📚 Legal Domain

The initial corpus focuses on Nigeria's 2025 tax reform framework, including:

- Nigeria Tax Act (NTA)
- Nigeria Tax Administration Act (NTAA)
- Nigeria Revenue Service Establishment Act (NRSEA)
- Joint Revenue Board Establishment Act (JRBA)
- Nigeria Revenue Service circulars, FAQs and notices
- Selected repealed legislation for negative/repeal detection tests

The project focuses particularly on:

- Company Income Tax
- Value Added Tax (VAT)
- PAYE
- Personal Income Tax
- SME taxation
- Withholding Tax
- Tax administration
- Current vs. repealed legislation

---

## 🧪 Evaluation

Kasai includes a dedicated legal evaluation benchmark rather than relying only on generic language-model benchmarks.

The evaluation covers:

| Category | Purpose |
|---|---|
| Factual Accuracy | Can the model retrieve the correct tax-law fact? |
| Legal Interpretation | Can it correctly interpret a provision? |
| Legal Reasoning | Can it reason through interacting provisions? |
| Citation Accuracy | Does it identify the correct statutory provision? |
| Citation Completeness | Does it provide the necessary supporting provisions? |
| Current-Law Recognition | Can it identify the legislation currently in force? |
| Repealed-Law Detection | Can it avoid relying on superseded legislation? |
| Temporal Reasoning | Can it distinguish rules across different periods? |
| Scenario/Application | Can it apply tax rules to a realistic scenario? |
| Abstention | Can it recognize when information is insufficient? |

### Repealed-Law Benchmark

A core component of Kasai is testing whether the model can recognize questions that deliberately reference **repealed legislation**.

For example:

```text
Question
   │
   ▼
Does the referenced legislation remain in force?
   │
   ├── Yes → Apply current law
   │
   └── No  → Identify/reject repealed framework
```

This is important because a legally fluent answer can still be **legally wrong** if it applies an outdated statute.

---

## 📊 Kasai v0.1 Results

The v0.1 evaluation contains **12 benchmark questions**.

The model demonstrated improved **Nigerian tax-domain alignment** compared with the untuned Gemma 3 4B model.

However, the evaluation also exposed important limitations:

- incorrect statutory citations;
- incorrect tax calculations in some scenarios;
- failures to reliably detect repealed legislation;
- inconsistent legal reasoning;
- occasional overconfident answers;
- incomplete abstention behavior;
- repetitive generation in some responses.

Therefore, Kasai v0.1 should be considered a **research prototype**, rather than a production-ready tax-law system.

---

## 🔬 Base Model vs Kasai

One objective of the project is to determine whether domain adaptation provides measurable improvement over the underlying general-purpose model.

The comparison uses the same evaluation questions against:

```text
Gemma 3 4B Instruct
        vs.
Kasai v0.1
```

The initial comparison showed that Kasai was more consistently oriented toward the **Nigerian tax domain**, while some factual and legal-reasoning errors remained.

This distinction is important:

> **Domain alignment ≠ legal reliability.**

Kasai's v0.1 results suggest that SFT can improve specialization, but additional grounding and verification mechanisms are required for reliable legal applications.

---



## 🚀 Running Kasai

Kasai v0.1 is distributed as a **LoRA adapter**, rather than a complete standalone model.

The adapter should be loaded on top of the compatible base model:

```text
google/gemma-3-4b-it
        +
Kasai LoRA Adapter
        ↓
Kasai v0.1
```

Example loading workflow:

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

base_model = AutoModelForCausalLM.from_pretrained(
    "google/gemma-3-4b-it"
)

tokenizer = AutoTokenizer.from_pretrained(
    "path/to/kasai_sft_v0.1"
)

model = PeftModel.from_pretrained(
    base_model,
    "path/to/kasai_sft_v0.1"
)
```

For the exact training and inference configuration, see the project notebook and model metadata.

---

## ⚠️ Limitations

Kasai v0.1 has several known limitations.

### 1. Legal accuracy

The model can produce confident but incorrect legal answers.

### 2. Citation reliability

A response may identify the correct concept while giving an incorrect statutory section.

### 3. Repealed-law detection

The model does not yet reliably recognize every reference to superseded legislation.

### 4. Limited training data

The initial SFT dataset contains only **96 records**, which is insufficient to comprehensively represent Nigerian tax law.

### 5. Evaluation size

The initial benchmark contains **12 questions** and should therefore be considered a pilot evaluation rather than a statistically comprehensive benchmark.

### 6. No production legal verification layer

Kasai v0.1 does not independently verify every generated legal claim against an authoritative, version-controlled legal database.

---

## 🔮 Future Work

Future versions can improve reliability through a combination of:

### Retrieval-Augmented Generation

```text
User Question
     ↓
Legal Query
     ↓
Retrieve authoritative provisions
     ↓
Current-law / repeal verification
     ↓
Kasai
     ↓
Answer + citations
```

### Additional improvements

- Larger and expert-reviewed SFT datasets
- More comprehensive Nigerian tax-law coverage
- Stronger repealed-law negative examples
- Citation verification
- Temporal/version-aware retrieval
- Legal reasoning datasets
- Better abstention training
- Human expert evaluation
- Automated regression testing
- RAG + SLM hybrid architecture
- Quantized deployment for resource-constrained environments

---

## 🛡️ Responsible AI

Kasai is designed around the following principles:

- **Accuracy**
- **Reliability**
- **Explainability**
- **Transparency**
- **Fairness**
- **Privacy**
- **Inclusivity**
- **Safety**

The system should not replace qualified tax professionals or authoritative legal sources.

When uncertainty is high, a future production version should prefer:

```text
"I don't have enough verified information to answer this reliably."
```

over a confident unsupported legal claim.

---

## 📄 Research Disclaimer

Kasai is an experimental research project.

**Kasai v0.1 is not a legal or tax advisory service and must not be relied upon for filing decisions, tax compliance, litigation, financial decisions, or other professional legal/tax matters.**

Always verify tax-law answers against the latest authoritative Nigerian legislation, regulations, and official guidance.

---

## 👥 Project

**Kasai — Nigerian Tax Law Small Language Model**

Built as an exploration of **domain-specific language models, legal AI, Nigerian tax-law reasoning, and responsible AI evaluation**.

---

## 📜 License

Add the project's chosen license here, for example:

```text
MIT License
```

> Note: the license for the Kasai project does not override the licensing terms of the underlying Gemma model or the Nigerian legal source materials.
