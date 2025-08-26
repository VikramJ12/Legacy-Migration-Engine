"""Streamlit front-end (app/streamlit_app.py)"""
import sys
from pathlib import Path
# ensure root is on path so `backend` package imports work
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from backend.parser import parse_c_file_to_ast_dict, parse_c_code_str_to_ast
from backend.ast_to_neo4j import push_ast_to_neo4j
from backend.vectorizer import attach_embeddings_to_nodes
from backend.llm_converter import convert_c_to_python
from backend.utils import ensure_outputs_dir
import ujson as json
from datetime import datetime

st.set_page_config(page_title='Legacy Migration Engine', layout='wide')
st.title('Legacy Migration Engine — C procedural → OOP Python')

with st.sidebar:
    st.markdown('## Controls')
    model_choice = st.text_input('LLM model (ollama)', 'llama3.2')  # default to llama3.2
    embed_model = st.text_input('Embedding model (ollama)', 'nomic-embed-text')

uploaded = st.file_uploader('Upload a C file', type=['c','h','txt'])
code = ''
if uploaded is not None:
    code = uploaded.getvalue().decode('utf-8')
else:
    code = st.text_area('Or paste C code here', height=300)

if st.button('Run migration'):
    if not code.strip():
        st.error('Please provide C code first')
    else:
        out_dir = ensure_outputs_dir('outputs')

        with st.spinner('Parsing C to AST...'):
            # parse string -> AST dict (if code small) else write to temp file and parse file
            try:
                ast = parse_c_code_str_to_ast(code)
            except Exception:
                # fallback: write temp file and call parse_file-based function
                tmp = out_dir / 'tmp_input.c'
                tmp.write_text(code)
                ast = parse_c_file_to_ast_dict(str(tmp))
            st.success('Parsed AST')

        with st.spinner('Pushing AST to Neo4j...'):
            root_id = push_ast_to_neo4j(ast)
            st.success(f'AST pushed to Neo4j (root id {root_id})')

        with st.spinner('Attaching embeddings (sample)...'):
            try:
                attach_embeddings_to_nodes(limit=200, model=embed_model)
            except Exception as e:
                st.warning(f'Embedding step had an issue: {e}')
            st.success('Embeddings attached (sample)')

        with st.spinner('Converting C to OOP Python using Ollama...'):
            try:
                py = convert_c_to_python(code, model=model_choice)
            except Exception as e:
                st.error(f'Conversion failed: {e}')
                py = ''
            st.success('Conversion complete')

        ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        ast_path = out_dir / f'ast_{ts}.json'
        gen_path = out_dir / f'generated_{ts}.py'
        ast_path.write_text(json.dumps(ast, indent=2))
        gen_path.write_text(py)

        st.subheader('Generated Python')
        st.code(py if py else '# conversion failed', language='python')
        st.download_button('Download generated .py', data=py, file_name=gen_path.name, mime='text/x-python')

        st.subheader('AST (JSON)')
        st.json(ast)
        st.download_button('Download AST JSON', data=json.dumps(ast, indent=2), file_name=ast_path.name)

        st.info('Neo4j contains AST nodes labeled :ASTNode and relationships :CHILD')

st.markdown('---')
st.caption('This is a demo pipeline — adjust models, batching, and safety checks per your needs.')

