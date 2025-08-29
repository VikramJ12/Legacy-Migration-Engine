"""Attach embeddings to ASTNode nodes using Ollama embeddings and save into Neo4j."""
import ollama
ollama.api_url = "http://host.docker.internal:11434"

from .neo4j_client import run_cypher
import math
import ast

def embed_text(text: str, model: str = 'nomic-embed-text:latest') -> list:
    """
    Call ollama embeddings. Converts returned response into a float list.
    """
    try:
        resp = ollama.embeddings(model=model, prompt=text)
        print("Ollama response:", resp)
    except Exception as e:
        raise RuntimeError(f"Ollama embeddings call failed: {e}")

    # If response is a string like "embedding=[...]", parse it
    if isinstance(resp, str) and resp.startswith("embedding="):
        try:
            # Extract the list part and parse it safely
            embedding_str = resp[len("embedding="):]
            embedding = ast.literal_eval(embedding_str)
            return [float(x) for x in embedding]
        except Exception as e:
            raise RuntimeError(f"Failed to parse embedding string: {e}")

    # resp might be a dict or list depending on ollama client version
    if isinstance(resp, dict):
        # standard key
        if 'embedding' in resp and isinstance(resp['embedding'], list):
            return [float(x) for x in resp['embedding']]
        # outputs
        if 'outputs' in resp and isinstance(resp['outputs'], list):
            for out in resp['outputs']:
                if 'embedding' in out:
                    return [float(x) for x in out['embedding']]
        # fallback: search for any list of numbers
        for v in resp.values():
            if isinstance(v, list) and all(isinstance(x, (int,float)) for x in v):
                return [float(x) for x in v]
    elif isinstance(resp, list):
        return [float(x) for x in resp]

    raise RuntimeError("Unexpected embedding response from Ollama")

def attach_embeddings_to_nodes(limit: int = 200, model: str = 'nomic-embed-text:latest'):
    rows = run_cypher('MATCH (n:ASTNode) RETURN n.node_id AS node_id, n.nodetype AS nodetype, n.name AS name LIMIT $limit', {'limit': limit})
    for r in rows:
        node_id = r['node_id']
        nodetype = r.get('nodetype', '')
        name = r.get('name', '')
        text = f"AST node type: {nodetype}. name: {name}"
        emb = embed_text(text, model=model)
        # store embedding
        run_cypher('MATCH (n:ASTNode {node_id:$node_id}) SET n.embedding = $emb', {'node_id': node_id, 'emb': emb})

if __name__ == '__main__':
    attach_embeddings_to_nodes()

