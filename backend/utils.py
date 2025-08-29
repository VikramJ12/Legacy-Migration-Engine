import os
from pathlib import Path
from dotenv import load_dotenv
from backend.neo4j_client import run_cypher

def load_env(env_path: str = None):
    if env_path:
        load_dotenv(env_path)
    else:
        load_dotenv()

def ensure_outputs_dir(path='outputs'):
    p = Path(path)
    p.mkdir(exist_ok=True)
    return p

def delete_graph_instance(instance_id: str):
    """
    Delete all nodes and relationships that were created for a given migration instance.
    """
    query = "MATCH (n) WHERE n.instance_id = $instance_id DETACH DELETE n"
    params = {'instance_id': instance_id}
    run_cypher(query, params)

