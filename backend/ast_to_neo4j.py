"""Push AST dict into Neo4j as nodes and CHILD relationships."""
import uuid
from backend.neo4j_client import run_cypher
import ujson as json
from typing import Dict, Any

def visit(node, instance_id, parent_id=None):
    # Ensure each node has a unique id.
    node_id = node.get("id")
    if not node_id:
        node_id = str(uuid.uuid4())
        node["id"] = node_id

    # Build properties from all keys except 'children'
    props = {k: v for k, v in node.items() if k != "children"}

    query = """
    MERGE (n:ASTNode {node_id: $node_id})
    SET n += $props, n.migration_id = $instance_id
    """
    params = {'node_id': node_id, 'props': props, 'instance_id': instance_id}
    run_cypher(query, params)

    # If there's a parent, create the relationship from parent to current node.
    if parent_id:
        rel_query = """
        MATCH (p:ASTNode {node_id: $parent_id}), (c:ASTNode {node_id: $child_id})
        MERGE (p)-[:CHILD]->(c)
        """
        rel_params = {'parent_id': parent_id, 'child_id': node_id}
        run_cypher(rel_query, rel_params)

    # Process children if present, and pass current node id as parent_id.
    for child in node.get("children", []):
        visit(child, instance_id, parent_id=node_id)
    return node_id

def push_ast_to_neo4j(ast_dict: dict, instance_id: str):
    """
    Recursively push AST nodes into Neo4j with a migration instance identifier.
    """
    return visit(ast_dict, instance_id)

if __name__ == '__main__':
    import sys, pathlib
    if len(sys.argv) < 2:
        print("Usage: python backend/ast_to_neo4j.py path/to/ast.json")
        raise SystemExit(1)
    ast = json.loads(open(sys.argv[1]).read())
    root = push_ast_to_neo4j(ast, "demo-instance")
    print("root node id", root)

