"""Convert C code to OOP Python using Ollama LLaMA 3.2 with AST context from Neo4j."""
import ollama
from backend.parser import parse_c_file_to_ast_dict, parse_c_code_str_to_ast
from backend.neo4j_client import run_cypher
import ujson as json
from typing import Optional
import re
import os
import requests

# default model (change if you prefer another installed model)
# DEFAULT_MODEL = 'llama3.2'
DEFAULT_MODEL = 'llama3.2'
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-8b-8192"

def get_top_ast_context(limit: int = 20) -> str:
    rows = run_cypher('MATCH (n:ASTNode) RETURN n.node_id AS id, n.nodetype AS nodetype, n.name AS name LIMIT $l', {'l': limit})
    snippets = []
    for r in rows:
        snippets.append(f"- {r.get('nodetype','')}: {r.get('name','')}")
    return '\n'.join(snippets)

def extract_text_from_ollama_response(resp) -> str:
    # Ollama client returns different shapes across versions; support common ones
    if isinstance(resp, dict):
        if 'response' in resp and isinstance(resp['response'], str):
            return resp['response']
        if 'text' in resp and isinstance(resp['text'], str):
            return resp['text']
        if 'outputs' in resp and isinstance(resp['outputs'], list):
            # find first output with 'content' or 'text'
            for out in resp['outputs']:
                if isinstance(out, dict):
                    for k in ('content','text'):
                        if k in out and isinstance(out[k], str):
                            return out[k]
        # try to stringify
        return json.dumps(resp)
    # if string directly
    if isinstance(resp, str):
        return resp
    return str(resp)

def convert_c_to_python(code: str, model: str = DEFAULT_MODEL, top_k_context: int = 30) -> str:
    """
    Convert C source `code` to OOP Python code. Uses short AST context pulled from Neo4j.
    Tries Groq first, falls back to Ollama if Groq fails.
    """
    context = get_top_ast_context(limit=top_k_context)

    system_prompt = (
        "You are an expert engineer that converts procedural C code into readable, well-structured OOP Python 3 code.\n"
        "Rules:\n"
        "1) Convert C structs with related functions into Python classes.\n"
        "2) Preserve naming where appropriate and document behavior with docstrings.\n"
        "3) Provide a short mapping summary of how C constructs map to Python (at top).\n        "
        "4) Return only the Python source code (no back-and-forth commentary).\n"
    )

    user_message = f"// AST context:\n{context}\n\n// C Source:\n{code}\n\n// Conversion instructions:\nConvert the above C into OOP Python with classes, methods, and clear docstrings. Output valid Python code."

    # Try Groq first
    if GROQ_API_KEY:
        try:
            print("Trying Groq for code generation...")
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": GROQ_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                "max_tokens": 2048,
                "temperature": 0.2
            }
            resp = requests.post(GROQ_CHAT_URL, headers=headers, json=data, timeout=60)
            resp.raise_for_status()
            result = resp.json()
            code = result['choices'][0]['message']['content']
            print("Using Groq for code generation.")
            python_code = extract_python_code(code)
            return python_code
        except Exception as e:
            print(f"Groq code generation failed: {e}")

    # Fallback to Ollama
    print("Falling back to Ollama for code generation...")
    try:
        resp = ollama.chat(model=model, messages=[{"role":"system", "content": system_prompt},
                                                 {"role":"user", "content": user_message}])
    except Exception as e:
        # fallback: try generate
        try:
            resp = ollama.generate(model=model, prompt=system_prompt + "\n\n" + user_message)
        except Exception as e2:
            raise RuntimeError(f"Ollama call failed: {e} / {e2}")

    text = extract_text_from_ollama_response(resp)
    python_code = extract_python_code(text)
    return python_code

def extract_python_code(text: str) -> str:
    """
    Extracts the first Python code block from a string.
    """
    # Look for triple-backtick python code block
    match = re.search(r"```python(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # Fallback: look for any code block
    match = re.search(r"```(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # Fallback: return the whole text
    return text.strip()

def generate_python_code(prompt: str) -> str:
    if GROQ_API_KEY:
        try:
            print("Trying Groq for code generation...")
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": GROQ_MODEL,
                "messages": [
                    {"role": "system", "content": "Convert C code to clean, idiomatic OOP Python. Only output Python code."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 2048,
                "temperature": 0.2
            }
            resp = requests.post(GROQ_CHAT_URL, headers=headers, json=data, timeout=60)
            resp.raise_for_status()
            result = resp.json()
            code = result['choices'][0]['message']['content']
            print("Using Groq for code generation.")
            return code
        except Exception as e:
            print(f"Groq code generation failed: {e}")

    # Fallback to Ollama (your existing code here)
    print("Falling back to Ollama for code generation...")
    context = get_top_ast_context(limit=30)

    system_prompt = (
        "You are an expert engineer that converts procedural C code into readable, well-structured OOP Python 3 code.\n"
        "Rules:\n"
        "1) Convert C structs with related functions into Python classes.\n"
        "2) Preserve naming where appropriate and document behavior with docstrings.\n"
        "3) Provide a short mapping summary of how C constructs map to Python (at top).\n        "
        "4) Return only the Python source code (no back-and-forth commentary).\n"
    )

    user_message = f"// AST context:\n{context}\n\n// C Source:\n{prompt}\n\n// Conversion instructions:\nConvert the above C into OOP Python with classes, methods, and clear docstrings. Output valid Python code."

    try:
        resp = ollama.chat(model=DEFAULT_MODEL, messages=[{"role":"system", "content": system_prompt},
                                                 {"role":"user", "content": user_message}])
    except Exception as e:
        # fallback: try generate
        try:
            resp = ollama.generate(model=DEFAULT_MODEL, prompt=system_prompt + "\n\n" + user_message)
        except Exception as e2:
            raise RuntimeError(f"Ollama call failed: {e} / {e2}")

    text = extract_text_from_ollama_response(resp)
    python_code = extract_python_code(text)
    return python_code

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python backend/llm_converter.py path/to/file.c")
        raise SystemExit(1)
    code = open(sys.argv[1]).read()
    out = convert_c_to_python(code)
    print(out)

