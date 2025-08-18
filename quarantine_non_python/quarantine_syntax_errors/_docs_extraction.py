"""Clean replacement for corrupted _docs_extraction.py module."""

import ast
import inspect
import textwrap
from typing import Any, Optional


class DocstringVisitor(ast.NodeVisitor):
    """Visitor to extract docstrings from AST nodes."""

    def __init__(self) -> None:
        super().__init__()
        self.target: Optional[str] = None
        self.attrs: dict[str, str] = {}
        self.previous_node_type: Optional[type[ast.AST]] = None

    def visit(self, node: ast.AST) -> Any:
        """Visit an AST node."""
        node_result = super().visit(node)
        self.previous_node_type = type(node)
        return node_result

    def visit_AnnAssign(self, node: ast.AnnAssign) -> Any:
        """Visit an annotated assignment node."""
        if isinstance(node.target, ast.Name):
            pass
        return self.generic_visit(node)


def extract_docstring(obj: Any) -> Optional[str]:
    """Extract docstring from an object."""
    try:
        return inspect.getdoc(obj)
    except Exception:
        return None


def format_docstring(docstring: str) -> str:
    """Format a docstring by removing excess whitespace."""
    if not docstring:
        return ""
    return textwrap.dedent(docstring).strip()


def extract_function_signature(func: Any) -> Optional[str]:
    """Extract function signature as string."""
    try:
        return str(inspect.signature(func))
    except Exception:
        return None
