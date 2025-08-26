"""
backend/parser.py
Parse C source into a JSON-serializable AST using pycparser.
Note: pycparser expects preprocessed-like input. Using fake_libc_include avoids most header issues.
"""
from pycparser import parse_file, c_parser, c_ast
import ujson as json
from pathlib import Path
import pycparser
import os

def parse_c_file_to_ast_dict(path: str) -> dict:
    """
    Parse C source file at `path` into nested dict AST.
    This will invoke the cpp preprocessor (via parse_file) using pycparser's fake_libc_include.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    fake_inc = os.path.join(os.path.dirname(pyccpath()), 'utils', 'fake_libc_include') \
        if False else None

def pyccpath():
    # helper to compute pycparser path
    import pycparser
    return pycparser.__file__

# We'll implement with a safe parse_file invocation using fake_libc_include
def parse_c_file_to_ast_dict(path: str) -> dict:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    # find fake_libc_include
    import pycparser
    fake_include = Path(pyccpath()).parent / 'utils' / 'fake_libc_include'
    cpp_args = [f"-I{str(fake_include)}"]

    ast = parse_file(str(path), use_cpp=True, cpp_args=cpp_args)

    def node_to_dict(node):
        if node is None:
            return None
        result = {'nodetype': type(node).__name__}
        # capture a few useful attributes
        for attr in getattr(node, 'attr_names', []):
            try:
                val = getattr(node, attr)
                result[attr] = str(val)
            except Exception:
                result[attr] = None
        # common names
        for key in ('name', 'declname', 'coord', 'type'):
            if hasattr(node, key):
                try:
                    result[key] = str(getattr(node, key))
                except Exception:
                    result[key] = None
        # children
        children = []
        for _, child in node.children():
            children.append(node_to_dict(child))
        if children:
            result['children'] = children
        return result

    return node_to_dict(ast)

def parse_c_code_str_to_ast(code: str) -> dict:
    """
    Use CParser directly for strings (not recommended for headers).
    """
    parser = c_parser.CParser()
    ast = parser.parse(code)
    def node_to_dict(node):
        if node is None:
            return None
        result = {'nodetype': type(node).__name__}
        for attr in getattr(node, 'attr_names', []):
            try:
                result[attr] = getattr(node, attr)
            except Exception:
                result[attr] = None
        children = []
        for _, child in node.children():
            children.append(node_to_dict(child))
        if children:
            result['children'] = children
        for key in ('name', 'declname', 'coord', 'type'):
            if hasattr(node, key):
                try:
                    result[key] = str(getattr(node, key))
                except Exception:
                    result[key] = None
        return result
    return node_to_dict(ast)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python backend/parser.py path/to/file.c")
        raise SystemExit(1)
    ast = parse_c_file_to_ast_dict(sys.argv[1])
    print(json.dumps(ast, indent=2))

