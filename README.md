# Synthetic Rectal Cancer MRI Reports Dataset and Generation Framework

This repository provides a fully synthetic dataset of paired structured and free-text primary-staging rectal cancer MRI reports, 
together with the reproducible framework used to generate, diversify, narrativise, audit, and evaluate the data.

Each case contains a structured report and a corresponding free-text radiology narrative. The dataset is intended for research in radiology NLP, report generation, information extraction, schema-constrained extraction, and structured-to-free-text alignment without exposing patient data.

All cases are synthetic and are not intended for clinical decision-making.

## Citation

Batrakova, M., Santinha, J., & Simões, A. M. (2026). *Synthetic Dataset of
Structured and Free-Text Primary Staging Rectal Cancer MRI Reports* [Data
set]. Zenodo.
[https://doi.org/10.5281/zenodo.21173484](https://doi.org/10.5281/zenodo.21173484)

## Pipeline

The pipeline has four stages:

1. **Generate structured reports**
   - `code_to_obtain_SR_data/synthetic_SR_dataset.ipynb`
   - Generates 100,000 fictitious structured reports.
   - Selects a reproducible, balanced subset of 1,000 reports.
   - Writes `balanced_synthetic_SR.jsonl`.

2. **Diversify the structured reports**
   - `code_to_obtain_SR_data/diversify_balanced_synthetic_SR.ipynb`
   - Introduces controlled missing values.
   - Removes unused structured fields.
   - Converts selected centimetre measurements to millimetres.
   - Writes the processed and modified JSONL datasets.

3. **Generate free-text reports**
   - `gpt4_freetext_reports.py`
   - Reads `balanced_synthetic_SR_modified.jsonl`.
   - Uses `gpt-4.1-2025-04-14` with `prompts/gpt4_prompt.py`.
   - Writes `generated_datasets/synthetic_reports_gpt4.csv`.

4. **Assess and correct report alignment**
   - `ds_assessment.py`
   - Uses `deepseek-reasoner` with `prompts/ds_prompts.py`.
   - Classifies each narrative as `Perfect`, `Minor issues`, or
     `Major issues`.
   - Generates a corrected narrative for reports classified as
     `Major issues`.
   - Updates `generated_datasets/ds_assessment_results.csv` in place.

## Repository layout

```text
synthetic_dataset/
├── code_to_obtain_SR_data/
│   ├── synthetic_SR_dataset.ipynb
│   ├── diversify_balanced_synthetic_SR.ipynb
│   └── jsonl_data/
│       ├── synthetic_SR_100000.jsonl
│       ├── balanced_synthetic_SR.jsonl
│       ├── balanced_synthetic_SR_processed.jsonl
│       └── balanced_synthetic_SR_modified.jsonl
├── generated_datasets/
│   ├── synthetic_reports_gpt4.csv
│   ├── ds_assessment_results.csv
│   └── updated_synthetic_dataset.csv
├── radiologist_assessment/
│   ├── anatomical_rules_assessment.docx
│   └── 20_synthetic_pairs_checked.docx
├── llm_benchmark_example/
│   ├── llama8b_outlines.ipynb
│   ├── prompt.py
│   └── pydantic_template.py
├── prompts/
│   ├── gpt4_prompt.py
│   └── ds_prompts.py
├── requirements.txt
├── gpt4_freetext_reports.py
└── ds_assessment.py
```

## Dataset files

The current CSV files contain 1,000 report pairs.

| File | Purpose | Columns |
| --- | --- | --- |
| `synthetic_reports_gpt4.csv` | Initial generated narratives by gpt-4.1 model| `synthetic_structured_report`, `free_text_report` |
| `ds_assessment_results.csv` | Alignment assessments and corrected narratives by deepseek r1 model| `synthetic_structured_report`, `free_text_report`, `ds_assessment`, `ds_corrected` |
| `updated_synthetic_dataset.csv` | Curated two-column dataset | `structured_report`, `free_text_report` |

The structured report is stored as a JSON object serialized inside a CSV
field. For the complete structured-report schema, see [SCHEMA.md](SCHEMA.md).

## Zero-shot structured-output benchmark

The `llm_benchmark_example/` directory contains a zero-shot benchmark for
extracting schema-constrained JSON from the synthetic free-text reports with
Llama 3.1 8B Instruct and Outlines:

- `llama8b_outlines.ipynb` loads
  `generated_datasets/updated_synthetic_dataset.csv`, runs zero-shot
  extraction, records inference time, and writes
  `generated_datasets/llm_benchmark_outputs/llama3_1_8b_zero_shot.csv`;
- `prompt.py` defines the zero-shot extraction prompt;
- `pydantic_template.py` defines the 25-field structured-output schema.

The original inference was run on premises in a Docker container using an
NVIDIA RTX A6000 GPU. A similar experiment can be conducted in Google Colab
with a GPU runtime. In the notebook, update `MODEL_NAME_OR_PATH` and uncomment
the CUDA diagnostics and model-loading cell before running the benchmark.

## Radiologist assessment

The `radiologist_assessment/` directory contains an expert qualitative review
contributed by Ana Miguel Simões, Radiology Resident at ULS Trás-os-Montes e
Alto Douro:

- `anatomical_rules_assessment.docx` reviews the structured-report template
  and generation rules. It discusses tumour location, T staging, the anterior
  peritoneal reflection, adjacent-organ and sphincter involvement, MRF
  involvement, nodal staging, tumour deposits, EMVI, and anatomical
  clock-face rules. It also proposes an updated staging template and comments
  on example reports.
- `20_synthetic_pairs_checked.docx` reviews 20 structured-report/free-text
  pairs for direct correspondence, narrative quality, and clinical
  plausibility. It records case-specific discrepancies and recommendations
  about terminology, anatomy, staging, and report style. That assessment is then used to correct the pipeline

These documents provide targeted expert feedback on the generation rules and
a sample of report pairs. They do not constitute clinical validation of all
1,000 records, and not every recommendation in the documents is necessarily
implemented in the current dataset.

## Setup

Python 3.10 or later is recommended.

```bash
python -m venv .venv
```

Activate the environment, then install the required packages:

```bash
python -m pip install -r requirements.txt
```

Create a local `.env` file:

```dotenv
OPENAI_API=your_openai_api_key
DS_API=your_deepseek_api_key
```

Do not commit API keys.

CSV and JSONL artifacts are tracked with Git LFS:

```bash
git lfs install
git lfs pull
```

## Running the pipeline

Run the notebooks in this order:

1. `code_to_obtain_SR_data/synthetic_SR_dataset.ipynb`
2. `code_to_obtain_SR_data/diversify_balanced_synthetic_SR.ipynb`

Then generate narratives:

```bash
python gpt4_freetext_reports.py
```

Before running the assessment stage,
`generated_datasets/ds_assessment_results.csv` must contain these columns:

```text
synthetic_structured_report,free_text_report,ds_assessment,ds_corrected
```

The first two columns can be initialized from
`synthetic_reports_gpt4.csv`; the assessment columns may initially be empty.

Run the assessment and correction stage:

```bash
python ds_assessment.py
```

Both API-backed scripts make one or more remote model calls per report.
Review expected API cost and rate limits before processing the full dataset.

## Reproducibility and validation

The notebooks use explicit random seeds for generation, balancing,
missing-value injection, and unit conversion. Re-running the same notebook
versions in order should reproduce the corresponding JSONL artifacts.

Recommended validation after modifying the dataset:

- confirm all structured-report fields contain valid JSON;
- confirm row counts and row order remain aligned across related files;
- compare structured and free-text findings report by report;
- verify MRF distance against MRF margin;
- verify lymph-node counts and extramesorectal locations;
- verify EMVI presence, clock position, and MRF involvement are mutually
  consistent.

## Limitations

- The reports are generated from the anatomically plausible rules in Python and 5 anonymized real rectal cancer mri reports were used for few-shot prompting. 
- The radiologist review covers the generation rules and a 20-report sample,
  not the complete dataset.
- (!) Synthetic distributions do not represent disease prevalence.
- Model-generated narratives can omit, alter, or invent findings. But from the studies and experiments we know, that "inverse inference" is a relatively easy and starightforward task for large language models. 
- Automated assessment is not a substitute for expert radiologist review.
- Prompt, model, and dependency changes can affect reproducibility.
