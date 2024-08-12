"""
This module provides functionality for generating documentation from Python source files.

It includes the DocGenerator class, which can extract docstrings from Python
files and convert them into a Markdown format for easy documentation generation
within the gitflow client subpackage.
"""

import importlib
import importlib.util
import sys
import os
import ast
from typing import List, NamedTuple

class DocItem(NamedTuple):
    """A named tuple representing a documentation item."""
    name: str
    doc: str
    lineno: int
    type: str

class DocGenerator:
    """
    A class for generating documentation from Python source files.

    This class provides methods to extract docstrings from Python files
    and convert them into a Markdown format.
    """

    @staticmethod
    def import_path(path):
        """Import a Python file from a given path."""
        module_name = os.path.basename(path).replace("-", "_")
        spec = importlib.util.spec_from_loader(
            module_name,
            importlib.machinery.SourceFileLoader(module_name, path),
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[module_name] = module
        return module

    @staticmethod
    def extract_docstrings(filename: str) -> List[DocItem]:
        """Extract docstrings from a Python file."""
        with open(filename, 'r') as file:
            node = ast.parse(file.read())

        module_doc = ast.get_docstring(node)
        all_docs = [DocItem("Module", module_doc, 0, "module")] if module_doc else []

        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.ClassDef)):
                doc = ast.get_docstring(item)
                if doc:
                    all_docs.append(DocItem(item.name, doc, item.lineno, type(item).__name__))
                if isinstance(item, ast.ClassDef):
                    for method in item.body:
                        if isinstance(method, ast.FunctionDef):
                            method_doc = ast.get_docstring(method)
                            if method_doc:
                                all_docs.append(DocItem(f"{item.name}.{method.name}", method_doc, method.lineno, "method"))

        all_docs.sort(key=lambda x: x.lineno)
        return all_docs

    @staticmethod
    def convert_to_markdown(docstrings: List[DocItem], filename: str, title: str, toc: bool) -> str:
        """Convert extracted docstrings to Markdown format."""
        base_name = os.path.splitext(os.path.basename(filename))[0]
        content = f"# {title or base_name}\n\n"

        if toc:
            content += "## Table of Contents\n\n"
            for i, doc_item in enumerate(docstrings, 1):
                anchor = doc_item.name.lower().replace(" ", "-").replace(".", "")
                content += f"{i}. [{doc_item.name}](#{anchor})\n"
            content += "\n"

        for doc_item in docstrings:
            if doc_item.type == "module":
                content += doc_item.doc.strip() + "\n\n"
            else:
                content += f"## {doc_item.name}\n\n"
                content += doc_item.doc.strip() + "\n\n"

        return content

    @classmethod
    def generate_doc(cls, filename: str, title: str = None, toc: bool = False) -> str:
        """Generate documentation for a Python file."""
        module = cls.import_path(filename)
        docstrings = cls.extract_docstrings(filename)
        return cls.convert_to_markdown(docstrings, filename, title, toc)
