"""
backend/parser.py
Parse C source into a JSON-serializable AST using libclang.
"""
import clang.cindex
import ujson as json
from pathlib import Path
import os

# You may need to tell clang where to find its library file.
# clang.cindex.Config.set_library_file('/usr/lib/x86_64-linux-gnu/libclang-14.so')

def parse_c_file_to_ast_dict(path: str) -> dict:
    """
    Parse C source file at `path` into a nested dict AST using libclang.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    index = clang.cindex.Index.create()
    
    # Add the directory of the file being parsed to the include path
    # This allows clang to find local header files (e.g., #include "tg.h")
    args = [f'-I{path.parent.resolve()}']

    tu = index.parse(str(path), args=args)

    # Check for parsing errors
    has_errors = False
    for diag in tu.diagnostics:
        if diag.severity >= clang.cindex.Diagnostic.Error:
            print(f"Error parsing file: {diag.spelling}")
            has_errors = True
    
    if has_errors:
        print("Parsing failed. Please check the errors above.")
        # Decide how to handle errors, e.g., return None or an empty dict
        return {}

    def node_to_dict_iterative(node):
        """
        Iterative traversal of the AST to avoid recursion depth issues.
        """
        if not node:
            return None

        root_dict = {
            'kind': node.kind.name,
            'spelling': node.spelling,
            'location': str(node.location.file),
            'line': node.location.line,
            'column': node.location.column,
            'type': node.type.spelling,
            'usr': node.get_usr(),
            'children': []
        }
        
        # Stack for iterative traversal, storing (node, parent_dict)
        stack = [(node, root_dict)]

        while stack:
            current_node, parent_dict = stack.pop()

            # Process children in reverse order to maintain original order in the output
            for child_node in reversed(list(current_node.get_children())):
                child_dict = {
                    'kind': child_node.kind.name,
                    'spelling': child_node.spelling,
                    'location': str(child_node.location.file),
                    'line': child_node.location.line,
                    'column': child_node.location.column,
                    'type': child_node.type.spelling,
                    'usr': child_node.get_usr(),
                    'children': []
                }
                parent_dict['children'].insert(0, child_dict)
                stack.append((child_node, child_dict))

        return root_dict


    return node_to_dict_iterative(tu.cursor)


def parse_c_code_str_to_ast(code: str, filename='temp.c') -> dict:
    """
    Use libclang to parse a string of C code.
    """
    index = clang.cindex.Index.create()
    tu = index.parse(filename, args=[], unsaved_files=[(filename, code)])

    def node_to_dict(node):
        if node is None:
            return None
            
        children = [node_to_dict(c) for c in node.get_children()]

        result = {
            'kind': node.kind.name,
            'spelling': node.spelling,
            'location': str(node.location.file),
            'line': node.location.line,
            'column': node.location.column,
            'type': node.type.spelling,
            'usr': node.get_usr(),
        }

        if children:
            result['children'] = children
        return result

    return node_to_dict(tu.cursor)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python backend/parser.py path/to/file.c")
        raise SystemExit(1)
    ast = parse_c_file_to_ast_dict(sys.argv[1])
    print(json.dumps(ast, indent=2))