# OncoGraphRAG
### Hybrid Knowledge Graph and Vector Retrieval for Oncology Research

OncoGraphRAG is a research prototype exploring how **knowledge graph representations, vector-based document retrieval, and benchmark-driven evaluation** can be combined to support evidence-grounded information retrieval and response generation in oncology.

The project brings together oncology handbook retrieval using ChromaDB, a graph construction pipeline based on PrimeKG, and an evaluation workflow for examining the quality and evidence alignment of generated responses.

> **Project status:** Research prototype. The repository contains experimental notebooks and graph-building code. The degree of integration between these components may vary as development continues.

---

## Table of Contents

- [Overview](#overview)
- [Motivation](#motivation)
- [Key Components](#key-components)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Component Workflows](#component-workflows)
- [Evaluation Approach](#evaluation-approach)
- [Configuration and API Keys](#configuration-and-api-keys)
- [Data and Reproducibility](#data-and-reproducibility)
- [Limitations](#limitations)
- [Future Work](#future-work)
- [Disclaimer](#disclaimer)
- [Acknowledgements](#acknowledgements)

---

## Overview

Retrieval-Augmented Generation (RAG) allows language models to generate responses using information retrieved from external knowledge sources. However, document retrieval and language generation alone do not guarantee that a response is complete, factually supported, or consistent with relevant relationships between biomedical entities.

OncoGraphRAG explores two complementary representations of oncology knowledge:

- **Vector retrieval:** Retrieves semantically relevant text from oncology reference material.
- **Knowledge graphs:** Represents entities and their relationships as a directed graph, enabling structured exploration of biomedical connections.

A separate evaluation workflow examines generated oncology responses against reference cases and evaluates selected aspects of evidence alignment.

The overarching research question is:

**Can combining unstructured-document retrieval with structured biomedical knowledge improve the evidence grounding and evaluability of oncology-focused RAG systems?**

This repository provides the building blocks for investigating that question.

## Motivation

Oncology information can involve several interconnected elements, including:

- Cancer types and disease characteristics
- Biomarkers and molecular associations
- Diagnostic investigations and imaging
- Treatment-related entities and relationships
- Clinical workup considerations

A text passage may provide detailed information about one subject, while a knowledge graph can represent relationships among multiple entities. Exploring both representations may help identify complementary sources of evidence.

OncoGraphRAG investigates this approach while emphasizing evaluation rather than relying solely on fluent-looking model responses.

The project is intended for experimentation in biomedical information retrieval, knowledge representation, and RAG evaluation—not for clinical decision-making.

## Key Components

### 1. Oncology Document Retrieval

A notebook builds a ChromaDB vector database from an oncology handbook PDF.

The workflow includes:

- Extracting text from a PDF using PyMuPDF.
- Splitting extracted text into smaller chunks.
- Generating semantic embeddings with `abhinand/MedEmbed-large-v0.1`.
- Storing document representations in ChromaDB.
- Retrieving relevant passages for a query.

This component provides a document-based retrieval foundation for oncology-related questions.

### 2. PrimeKG Knowledge Graph Construction

The graph-building script reads PrimeKG's `kg.csv` dataset and constructs a directed NetworkX graph.

The script uses the entity names and relation field to create graph edges:

`x_name → y_name`

Each edge stores its relation as an attribute. The resulting graph is exported in GraphML format for later loading or inspection.

This component establishes a structured representation of biomedical relationships. The current graph-building script uses entity names as node identifiers, so entity disambiguation and preservation of the original entity metadata are potential areas for improvement.

### 3. Oncology RAG Benchmarking

The evaluation notebook contains oncology-oriented patient cases with reference information and evaluates selected aspects of generated responses.

The implemented evaluation logic includes:

- **Workup concordance:** Examines whether required workup items appear in a generated response.
- **Knowledge graph citation accuracy:** Checks whether selected knowledge graph entities are cited or mentioned in the generated text.
- **Reference-based assessment:** Uses predefined benchmark cases and expected information to support comparison.

The notebook also includes an LLM-as-a-Judge workflow. Its outputs should be interpreted as experimental evaluation signals, not as proof of clinical correctness.

### 4. Experimental Hybrid-RAG Direction

The project is designed around the complementary use of document retrieval and structured knowledge. A fully integrated pipeline would retrieve relevant handbook passages, use graph relationships where appropriate, and combine the resulting evidence for response generation.

The repository's separate components provide a foundation for this direction. Do not assume that every step in this end-to-end pipeline is already implemented or automatically connected.

---

## Architecture

The conceptual workflow is:

```text
                Oncology Query
                      |
          +-----------+-----------+
          |                       |
          v                       v
   Document Retrieval      Knowledge Graph
          |                 Exploration
          v                       |
   Relevant Passages              v
          |                 Graph Evidence
          +-----------+-----------+
                      |
                      v
          Evidence-Informed Context
                      |
                      v
             Response Generation
                      |
                      v
            Benchmark Evaluation
```

The diagram describes the intended hybrid-RAG workflow. The existing notebooks and graph-building script should be treated as separate experimental components unless the integration is explicitly implemented in the current codebase.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core implementation and experimentation |
| Jupyter Notebook | Interactive development and evaluation |
| ChromaDB | Vector storage and similarity retrieval |
| Sentence Transformers | Semantic embedding generation |
| MedEmbed | Biomedical text embedding model |
| PyMuPDF | PDF text extraction |
| LangChain text splitters | Document chunking |
| NetworkX | Directed graph construction and manipulation |
| pandas | Tabular dataset processing |
| GraphML | Graph serialization and interchange |
| Gemini API | LLM-based evaluation workflow, where configured |

Dependencies and model versions should be aligned with the imports and configurations in the notebooks and scripts.

## Repository Structure

The principal project artifacts include:

```text
OncoGraphRAG/
├── the-cancer-rag-working-finalbenchmarked-depth3_sendSneha.ipynb
├── building-chromadb-on-oxfordoncohandbook (1).ipynb
├── 01_build_primekg_graph.py
├── data/                  # Datasets, configured locally
├── artifacts/             # Generated indexes and graph files
├── requirements.txt       # Reproducible dependencies
└── README.md
```

The `data/`, `artifacts/`, and `requirements.txt` entries above are suggested organizational conventions; create them if they are not already present in the repository. Rename the notebooks to shorter, descriptive filenames if desired.

### Main files

**`building-chromadb-on-oxfordoncohandbook (1).ipynb`**

Explores document processing, embedding generation, ChromaDB indexing, and retrieval using an oncology handbook.

**`01_build_primekg_graph.py`**

Builds a directed NetworkX graph from PrimeKG's `kg.csv` file and exports the graph as GraphML. It imports project configuration from `onco_followup.config`, so the corresponding package and settings must be available for the script to run as written.

**`the-cancer-rag-working-finalbenchmarked-depth3_sendSneha.ipynb`**

Contains the oncology benchmark and response-evaluation workflow, including workup concordance and knowledge graph citation checks.

---

## Getting Started

### Prerequisites

- Python installed in a compatible environment.
- Jupyter Notebook or JupyterLab for running the notebooks.
- Access to the required datasets and reference material.
- Sufficient RAM and disk space for the embedding model, vector index, and graph.
- A Gemini API key if the selected evaluation cells call the Gemini service.

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd OncoGraphRAG
```

Replace `<YOUR_REPOSITORY_URL>` with the repository's actual clone URL.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Linux:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the dependencies required by the notebooks and scripts. The following is a starting point, not a verified lockfile:

```bash
pip install pandas networkx tqdm pymupdf chromadb \
  sentence-transformers langchain-text-splitters \
  jupyter
```

Install any additional packages imported by the benchmark notebook, including the relevant Gemini SDK, if required.

For reproducibility, create a `requirements.txt` from a tested environment and pin compatible versions rather than relying indefinitely on unpinned packages.

### 4. Prepare the data

Place the required files in the locations expected by the code or update the corresponding configuration.

The graph-building script expects PrimeKG's `kg.csv` at the configured path. The script refers to a preceding download step named `scripts/00_download_primekg.py`; if that script is not present in the repository, obtain the dataset through an authorized source and configure the path manually.

For the document retrieval notebook, provide the relevant PDF at the path expected by the notebook.

**Important:** Large datasets, generated indexes, model caches, and copyrighted reference PDFs should not automatically be committed to Git. Check the applicable terms before redistributing any source material.

### 5. Launch Jupyter

```bash
jupyter notebook
```

Open the notebooks and execute their cells in dependency order. Review file paths, model downloads, environment variables, and external-service requirements before running the complete workflow.

---

## Component Workflows

### A. Build the oncology vector database

1. Load the oncology handbook PDF.
2. Extract its text.
3. Split the text into manageable chunks.
4. Generate embeddings using the configured MedEmbed model.
5. Store the chunks and their vector representations in ChromaDB.
6. Submit a query and inspect the retrieved passages.

Inspect the notebook for the exact chunking parameters, collection configuration, persistence behavior, and query interface.

### B. Construct the PrimeKG graph

Ensure that the project configuration package and PrimeKG CSV are available. Then execute the graph-building script from the repository root:

```bash
python scripts/01_build_primekg_graph.py
```

Adjust the command if the script is stored at the repository root rather than under `scripts/`.

The script validates the presence of the expected `x_name`, `y_name`, and `relation` columns, builds a directed graph, reports the number of nodes and edges, and writes a GraphML artifact to the configured output location.

### C. Run the evaluation notebook

1. Open the benchmark notebook.
2. Check the model and API configuration.
3. Review the benchmark cases and reference answers.
4. Execute the evaluation cells in order.
5. Inspect the individual outputs and aggregate metrics, where available.

Record the model, prompt, retrieval settings, benchmark version, and evaluation configuration alongside results to make comparisons more meaningful.

---

## Evaluation Approach

OncoGraphRAG explores evaluation beyond whether a response sounds plausible.

### Workup concordance

The benchmark includes a function for checking whether required workup items are present in generated text.

This provides a measure of agreement with selected reference requirements. It does not establish that all clinically relevant investigations have been included or that the proposed workup is appropriate for an actual patient.

### Knowledge graph citation accuracy

The evaluation workflow checks for the presence of selected graph entities in generated responses.

This is a useful preliminary signal for entity-level evidence alignment, but mentioning an entity does not prove that the associated relationship is correct or that the graph supports the full claim.

### LLM-as-a-Judge evaluation

The notebook includes an LLM-based judging workflow. Such evaluations can help compare outputs, but may be affected by judge-model bias, prompt design, inconsistent scoring, and the quality of the reference cases.

### Recommended evaluation extensions

Future experiments could include:

- Retrieval Recall@k, Precision@k, and Mean Reciprocal Rank.
- Comparison of vector-only, graph-only, and hybrid retrieval.
- Entity and relation extraction accuracy.
- Claim-level evidence support and citation correctness.
- Completeness and contradiction checks against reference answers.
- Ablation studies for graph evidence and document evidence.
- Repeated runs to assess variability in model-based judging.

Only report metrics that have actually been implemented and measured. Do not describe proposed metrics as existing experimental results.

---

## Configuration and API Keys

The graph builder relies on project-specific configuration, while the benchmark notebook may use a Gemini API key for model-based evaluation.

Keep credentials outside notebooks and source files. Where supported by the implementation, configure credentials through environment variables:

```bash
export GEMINI_API_KEY="your_api_key_here"
```

Never commit a real key to GitHub. If a key has already been exposed in a public commit, revoke it and generate a replacement.

Some workflows may run locally without a paid API, while the Gemini-based evaluation may require API access subject to the provider's current limits and pricing. Review the notebook cells before execution; no assumption is made here that every workflow is free of external costs.

The MedEmbed model may also need to be downloaded and run locally, which requires sufficient disk space and memory.

---

## Data and Reproducibility

For meaningful experiments, document:

- The source and version of the PrimeKG dataset.
- The document edition and source used for retrieval.
- Text chunk size and overlap.
- Embedding model identifier and version.
- Vector-store configuration and retrieval parameters.
- Graph construction and entity-identification choices.
- Generation model, prompts, and decoding settings.
- Benchmark cases, reference answers, and evaluation logic.
- Software versions and hardware used.

Store generated artifacts separately from source code where practical. If results depend on external APIs or remotely hosted models, note that changes to those services may affect reproducibility.

### Data licensing

PrimeKG and the oncology reference material have their own access and licensing conditions. Verify the relevant terms before redistributing datasets, extracted text, or generated derivatives.

The Oxford Handbook of Oncology is copyrighted material. Do not upload or redistribute its full PDF or substantial extracted content without the necessary permission. Users should obtain reference material through legitimate channels.

---

## Limitations

This project is an experimental research prototype, with several important limitations:

- **Integration:** Separate notebooks and scripts do not by themselves establish a fully integrated end-to-end hybrid-RAG system.
- **Graph representation:** The current graph builder uses entity names as node identifiers, which may merge distinct entities with identical names and discard useful source metadata.
- **Evidence quality:** Retrieved passages and graph connections can be incomplete, outdated, or irrelevant to a particular query.
- **Evaluation coverage:** Checks for required terms or graph entities are narrower than full clinical correctness evaluation.
- **Model dependence:** Generated answers and LLM-based judgments can be inconsistent or incorrect.
- **Dataset coverage:** Results depend on the selected documents, graph version, benchmark cases, and reference answers.
- **Clinical applicability:** No claim is made that this system is clinically validated or safe for patient-care decisions.

These limitations are part of the motivation for more rigorous retrieval, evidence attribution, and evaluation experiments.

---

## Future Work

Potential directions for extending OncoGraphRAG include:

1. **Integrated hybrid retrieval:** Combine ChromaDB retrieval and graph-based evidence selection in a single query pipeline.
2. **Entity linking:** Preserve PrimeKG identifiers and entity types to reduce ambiguity caused by name-only nodes.
3. **Evidence attribution:** Link generated claims to retrieved document passages and relevant graph relationships.
4. **Comparative evaluation:** Benchmark vector-only, graph-only, and hybrid approaches under consistent conditions.
5. **Stronger metrics:** Evaluate retrieval quality, claim support, contradiction rates, and answer completeness.
6. **Reproducible experiments:** Add configuration files, dependency pins, benchmark result exports, and automated tests.
7. **Error analysis:** Categorize failures involving missing evidence, irrelevant retrieval, incorrect graph paths, and unsupported generation.

These are proposed extensions, not claims about currently completed functionality.

---

## Disclaimer

OncoGraphRAG is intended for educational and research purposes in information retrieval, knowledge graphs, and language-model evaluation.

It is **not a medical device, clinical decision-support system, or substitute for professional medical judgment**. Its outputs may be inaccurate, incomplete, or outdated. Do not use generated responses to diagnose conditions, select treatments, or make decisions about patient care.

---

## Acknowledgements

This project builds on work and resources from:

- **PrimeKG** for structured biomedical knowledge.
- **ChromaDB** for vector storage and retrieval.
- **Sentence Transformers and MedEmbed** for semantic representation of biomedical text.
- **NetworkX** for graph construction and manipulation.
- **PyMuPDF** and **LangChain text splitters** for document processing.

Please consult the respective projects and dataset providers for their original publications, licenses, and citation requirements.
