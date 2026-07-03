# Synthetic Rectal MRI Dataset

This repository generates a fully synthetic dataset of structured rectal MRI
staging reports and corresponding free-text radiology narratives. It is
intended for research on report generation, information extraction, and
structured-to-free-text alignment without exposing protected health
information.

The generated cases are synthetic and must not be used for clinical
decision-making.

## Pipeline

The pipeline has five stages:

0. **Define the anatomical rules**
   - Define the anatomically plausible rules verified by the radiologist to generate synthetic structured reports. 

2. **Generate structured reports**
   - `code_to_obtain_SR_data/synthetic_SR_dataset.ipynb`
   - Generates 100,000 fictitious structured reports.
   - Selects a reproducible, balanced subset of 1,000 reports.
   - Writes `balanced_synthetic_SR.jsonl`.

3. **Diversify the structured reports**
   - `code_to_obtain_SR_data/diversify_balanced_synthetic_SR.ipynb`
   - Introduces controlled missing values.
   - Removes unused structured fields.
   - Converts selected centimetre measurements to millimetres.
   - Writes the processed and modified JSONL datasets.

4. **Generate free-text reports**
   - `gpt4_freetext_reports.py`
   - Reads `balanced_synthetic_SR_modified.jsonl`.
   - Uses `gpt-4.1-2025-04-14` with `prompts/gpt4_prompt.py`.
   - Writes `generated_datasets/synthetic_reports_gpt4.csv`.

5. **Assess and correct report alignment**
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
│   └── jsonl_data_vscode/
│       ├── synthetic_SR_100000.jsonl
│       ├── balanced_synthetic_SR.jsonl
│       ├── balanced_synthetic_SR_processed.jsonl
│       └── balanced_synthetic_SR_modified.jsonl
├── generated_datasets/
│   ├── synthetic_reports_gpt4.csv
│   ├── ds_assessment_results.csv
│   └── updated_synthetic_dataset.csv
├── prompts/
│   ├── gpt4_prompt.py
│   └── ds_prompts.py
├── gpt4_freetext_reports.py
├── ds_assessment.py
└── test.py
```

## Dataset files

The current CSV files contain 1,000 report pairs.

| File | Purpose | Columns |
| --- | --- | --- |
| `synthetic_reports_gpt4.csv` | Initial generated narratives by gpt-4o model | `synthetic_structured_report`, `free_text_report` |
| `ds_assessment_results.csv` | Alignment assessments and corrected narratives woth DeepSeek R1 model| `synthetic_structured_report`, `free_text_report`, `ds_assessment`, `ds_corrected` |
| `updated_synthetic_dataset.csv` | Curated two-column dataset | `structured_report`, `free_text_report` |

The structured report is stored as a JSON object serialized inside a CSV
field. Its top-level sections are:

- `local_tumor_status`
- `mesorectal_fascia_involement`
- `lymph_nodes_and_tumor_deposits`
- `emvi`

The key `mesorectal_fascia_involement` retains its original spelling for
dataset compatibility.

## Setup

Python 3.10 or later is recommended.

```bash
python -m venv .venv
```

Activate the environment, then install the required packages:

```bash
pip install "pydantic>=2" openai python-dotenv jupyter
```

Create a local `.env` file:

```dotenv
OPENAI_API=your_openai_api_key
DS_API=your_deepseek_api_key
```

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

- The reports are generated from pre-define rules verified by the radiologist. 5 translated anonymized real reports are used for a few-shot prompting 
- Synthetic distributions do not represent disease prevalence.
- Model-generated narratives can omit, alter, or invent findings. But from the studies we know, that "inverse inference", i.e from structured data to free text, is relatively easy and straightforward task for large language models 
- Automated assessment is not a substitute for expert radiologist review.
- Prompt, model, and dependency changes can affect reproducibility.
