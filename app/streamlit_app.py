"""Streamlit front-end (app/streamlit_app.py)"""
import sys
import uuid
from pathlib import Path
from datetime import datetime

import streamlit as st

# ensure root is on path so `backend` package imports work
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.parser import parse_c_file_to_ast_dict, parse_c_code_str_to_ast
from backend.ast_to_neo4j import push_ast_to_neo4j  # update: should accept instance_id argument
from backend.vectorizer import attach_embeddings_to_nodes
from backend.llm_converter import convert_c_to_python
from backend.utils import ensure_outputs_dir, delete_graph_instance

st.set_page_config(page_title='Legacy Migration Engine', layout='wide')
st.title('Legacy Migration Engine — C procedural → OOP Python')

with st.sidebar:
    st.markdown('## Controls')
    model_choice = st.text_input('LLM model (ollama)', 'llama3.2')
    embed_model = st.text_input('Embedding model (ollama)', 'nomic-embed-text:latest')

# Accept multiple files so that we can decide on ephemeral graph vs. persistent graph
uploaded_files = st.file_uploader('Upload C file(s)', type=['c', 'h', 'txt'], accept_multiple_files=True)
# Allow paste input if no file is uploaded
if (uploaded_files is None) or (len(uploaded_files) == 0):
    code = st.text_area('Or paste C code here', height=300)
    files_to_process = []  # will process the single pasted code later
else:
    files_to_process = uploaded_files

if st.button('Run migration'):
    # Prepare output directory
    out_dir = ensure_outputs_dir('outputs')

    # Generate a unique migration instance id for this run
    instance_id = str(uuid.uuid4())
    st.info(f"Migration Instance ID: {instance_id}")

    # If files were uploaded, process all of them and accumulate their code
    # Otherwise, use the pasted code
    aggregated_ast = None
    if files_to_process:
        for file in files_to_process:
            code = file.read().decode('utf-8')
            try:
                ast = parse_c_code_str_to_ast(code)
            except Exception:
                tmp = out_dir / 'tmp_input.c'
                tmp.write_text(code)
                ast = parse_c_file_to_ast_dict(str(tmp))
            # Push AST to Neo4j with the instance tag (update backend function accordingly)
            push_ast_to_neo4j(ast, instance_id)
            # Optionally aggregate the ASTs if later needed for conversion
            if aggregated_ast is None:
                aggregated_ast = ast
            else:
                # Merge ASTs as appropriate (this is simplified)
                aggregated_ast['nodes'].extend(ast.get('nodes', []))
    else:
        # Use pasted code – treat as a single file
        if not code.strip():
            st.error('Please provide C code first')
            st.stop()
        try:
            ast = parse_c_code_str_to_ast(code)
        except Exception:
            tmp = out_dir / 'tmp_input.c'
            tmp.write_text(code)
            ast = parse_c_file_to_ast_dict(str(tmp))
        push_ast_to_neo4j(ast, instance_id)
        aggregated_ast = ast

    st.success('AST pushed to Neo4j')

    # Attach embeddings
    with st.spinner('Attaching embeddings (sample)...'):
        try:
            attach_embeddings_to_nodes(limit=2000, model=embed_model)
        except Exception as e:
            st.warning(f'Embedding step had an issue: {e}')
        st.success('Embeddings attached (sample)')

    # Convert C to Python using the aggregated code (or latest file's code)
    with st.spinner('Converting C to OOP Python using Ollama...'):
        try:
            # If multiple files, you might want to combine code in a custom way.
            # Here we simply use the code from the last processed file.
            py = convert_c_to_python(code, model=model_choice)
        except Exception as e:
            st.error(f'Conversion failed: {e}')
            py = ''
        st.success('Conversion complete')

    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    ast_path = out_dir / f'ast_{ts}.json'
    gen_path = out_dir / f'generated_{ts}.py'
    ast_path.write_text(str(aggregated_ast))
    gen_path.write_text(py)

    st.subheader('Generated Python')
    st.code(py if py else '# conversion failed', language='python')
    st.download_button('Download generated .py', data=py, file_name=gen_path.name, mime='text/x-python')

    st.subheader('AST (JSON)')
    st.json(aggregated_ast)
    st.download_button('Download AST JSON', data=str(aggregated_ast), file_name=ast_path.name)

    st.info('Neo4j contains AST nodes labeled :ASTNode and relationships :CHILD')

    # For a single file migration, delete the temporary graph instance after conversion.
    if (files_to_process and len(files_to_process) == 1) or (not files_to_process):
        delete_graph_instance(instance_id)
        st.info("Temporary AST graph for this migration instance has been deleted.")
    else:
        st.info("Graph created for the multi‐file migration instance (preserving inter‐file relations).")

st.markdown('---')
st.caption('This is a demo pipeline — adjust models, batching, and safety checks per your needs.')

