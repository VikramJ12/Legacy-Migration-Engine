"""Simple neo4j wrapper"""
from neo4j import GraphDatabase
import os
from typing import Optional, Iterable

NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'strongpass123')

_driver = None

def get_driver():
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    return _driver

def close_driver():
    global _driver
    if _driver:
        _driver.close()
        _driver = None

def run_cypher(query: str, params: Optional[dict] = None) -> Iterable:
    driver = get_driver()
    with driver.session() as session:
        result = session.run(query, params or {})
        # return generator of records (list-friendly)
        return list(result)

