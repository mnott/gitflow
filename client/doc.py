"""
This module provides functionality for generating documentation from Python source files.

It includes the DocGenerator class, which can extract docstrings from Python
files and convert them into a Markdown format for easy documentation generation.
"""

import importlib
import importlib.util
import sys
import os
import ast
from typing import List, Tuple, NamedTuple

class DocItem(NamedTuple):
    """
    A named tuple representing a documentation item.

    Attributes:
        name   (str): The name of the documented item (e.g., function or class name).
        doc    (str): The docstring of the item.
        lineno (int): The line number where the item is defined in the source file.
        type   (str): The type of the item (e.g., 'module', 'class', 'function', 'method').
    """
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
        """
        Import a Python file from a given path.

        Args:
            path (str): The path to the Python file.

        Returns:
            module: The imported module object.
        """
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
        """
        Extract docstrings from a Python file.

        Args:
            filename (str): The path to the Python file.

        Returns:
            List[DocItem]: A list of DocItem objects containing the extracted docstrings.
        """
        with open(filename, 'r') as file:
            lines = file.readlines()
            node = ast.parse(''.join(lines))

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
        """
        Convert extracted docstrings to Markdown format.

        Args:
            docstrings (List[DocItem]): The list of extracted docstrings.
            filename             (str): The name of the source file.
            title                (str): The title for the documentation.
            toc                 (bool): Whether to include a table of contents.

        Returns:
            str: The generated Markdown content.
        """
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
        """
        Generate documentation for a Python file.

        This method combines the extraction of docstrings and conversion to Markdown.

        Args:
            filename         (str): The path to the Python file.
            title  (str, optional): The title for the documentation. Defaults to the filename.
            toc   (bool, optional): Whether to include a table of contents. Defaults to False.

        Returns:
            str: The generated Markdown documentation.
        """
        module = cls.import_path(filename)
        docstrings = cls.extract_docstrings(filename)
        return cls.convert_to_markdown(docstrings, filename, title, toc)
