"""Push AST dict into Neo4j as nodes and CHILD relationships."""
import uuid
from backend.neo4j_client import run_cypher
import ujson as json
from typing import Dict, Any

def push_ast_to_neo4j(ast: Dict[str, Any], label='ASTNode') -> str:
    """
    Create nodes with properties: node_id, nodetype, name.
    Link parent -> child with :CHILD relationships.
    Returns the root node_id.
    """
    def visit(node: Dict[str, Any], parent_id: str = None) -> str:
        node_id = str(uuid.uuid4())
        nodetype = node.get('nodetype', '')
        name = node.get('name') or node.get('declname') or node.get('coord') or ''
        props = {'node_id': node_id, 'nodetype': nodetype, 'name': name}
        # create node
        run_cypher(f"MERGE (n:{label} {{node_id:$node_id}}) SET n += $props", {'node_id': node_id, 'props': props})
        # create relationship
        if parent_id:
            run_cypher("MATCH (p:{label} {{node_id:$parent}}), (c:{label} {{node_id:$child}}) MERGE (p)-[:CHILD]->(c)".format(label=label),
                       {'parent': parent_id, 'child': node_id})
        # children
        for child in node.get('children', []):
            visit(child, node_id)
        return node_id

    root_id = visit(ast, None)
    return root_id

if __name__ == '__main__':
    import sys, pathlib
    if len(sys.argv) < 2:
        print("Usage: python backend/ast_to_neo4j.py path/to/ast.json")
        raise SystemExit(1)
    ast = json.loads(open(sys.argv[1]).read())
    root = push_ast_to_neo4j(ast)
    print("root node id", root)

