# Legacy Migration Engine (local)

## What it does
- Parse C into AST (pycparser)
- Store AST in Neo4j
- Vectorize AST nodes (Ollama embeddings)
- Provide AST context to LLaMA3.2 (Ollama) to convert code to OOP Python
- Streamlit UI for upload/paste, visualize AST, download generated code

## Prerequisites
- Python 3.10+
- Neo4j running locally or remotely (bolt)
- Ollama installed locally (https://ollama.com)
- Models pulled to Ollama:
  - `ollama pull nomic-embed-text`
  - `ollama pull llama3.2`

## Install
```bash
git clone <your-repo> legacy-migration-engine
cd legacy-migration-engine
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

