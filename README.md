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
```

## How to use:

### 1. Build the image:
```bash
docker build -t legacy-migration-engine .
```

### 2. Run the container:
```bash
docker run -p 8501:8501 \
  -e NEO4J_URI=bolt://host.docker.internal:7687 \
  -e NEO4J_USER=neo4j \
  -e NEO4J_PASSWORD=yourpassword \
  -e GROQ_API_KEY=your_groq_api_key_here \
  legacy-migration-engine
```

### Note:
i) If Neo4j is running on your host, use host.docker.internal for NEO4J_URI inside Docker.
ii) You can override any environment variable at runtime with -e.

