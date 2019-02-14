# Copyright 2019 Alix Hamilton
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utility functions for working with Jupyter notebooks in Python."""

import os

import nbconvert
import nbformat

from nbsampleutils import preprocessors


def get_notebook_from_filepath(filepath):
    """Construct a nbformat.v4.NotebookNode from a local Jupyter notebook

    Args:
        filepath (str):
            Local path to the `.ipynb` file to open and use to construct a
            nbformat.v4.NotebookNode instance.

    Returns:
        nbformat.v4.NotebookNode: NotebookNode constructed from the `filepath`.
    """
    with open(filepath) as notebook_file:
        return nbformat.read(notebook_file, as_version=4)


def get_output_text(cell):
    """Returns the output text of a cell.

    Args:
        cell (nbformat.NotebookNode):
            A cell from a NotebookNode (ex. `notebook_node.cells[0]`)

    Returns:
        str:
            The string output of the cell, or an empty string if the cell does
            not have any outputs.
    """
    output_lines = []
    if "outputs" not in cell:
        return ""
    for output in cell.outputs:
        if "text" in output:
            output_lines.append(output.text)
        if "data" in output:
            if "text/plain" in output.data:
                output_lines.append(output.data["text/plain"])
    return "".join(output_lines)


def make_notebook_node(code_cell_contents):
    """Create a new notebook node from a list of code cell contents

    Args:
        code_cell_contents (list(str)):
            List of code cell contents to make up the cells of a new notebook.
            For example, `'print(2 + 2)'`.

    Returns:
        nbformat.v4.NotebookNode:
            A new notebook node with 1 code cell for each item in
            code_cell_contents.
    """
    cells = [
        nbformat.v4.new_code_cell(source=code) for code in code_cell_contents]
    notebook_node = nbformat.v4.new_notebook(cells=cells)
    return notebook_node


def run_from_filepath(
        filepath,
        input_string_replacements=None,
        **execute_kwargs
):
    """Utility to execute and export notebooks

    Args:
        filepath (str): Path to the notebook file to execute
        input_string_replacements (dict(str, str), optional):
            Mapping of strings in cell inputs to replace before the notebook is
            executed.
        execute_kwargs (dict, optional):
            Key word arguments to pass to
            ``nbconvert.preprocessors.execute.ExecutePreprocessor``.

    Returns:
        nbformat.NotebookNode: The executed notebook node.
    """
    notebook_path, _ = os.path.split(filepath)
    notebook_node = get_notebook_from_filepath(filepath)

    return run_notebook_node(
        notebook_node,
        notebook_path=notebook_path,
        input_string_replacements=input_string_replacements,
        **execute_kwargs)


def run_notebook_node(
        notebook_node,
        notebook_path=None,
        input_string_replacements=None,
        **execute_kwargs
    ):
    """Execute a notebook node

    Args:
        notebook_node (nbformat.v4.NotebookNode): A notebook node to execute
        notebook_path (str, optional):
            File path to use for executing the notebook.
        input_string_replacements (dict(str, str), optional):
            Mapping of strings in cell inputs to replace before the notebook is
            executed.
        execute_kwargs (dict, optional):
            Key word arguments to pass to
            ``nbconvert.preprocessors.execute.ExecutePreprocessor``.

    Returns:
        nbformat.NotebookNode: The executed notebook node.
    """
    # Create notebook resources, setting the path to run the notebook from
    if notebook_path:
        resources = {"metadata": {"path": notebook_path}}
    else:
        resources = {}

    # Replace input strings if applicable
    if input_string_replacements:
        preprocessor = preprocessors.ReplaceCodeInputStringsPreprocessor(
            string_replacements=input_string_replacements
        )
        preprocessor.preprocess(notebook_node, resources)

    processor = nbconvert.preprocessors.execute.ExecutePreprocessor(
        **execute_kwargs)
    processor.preprocess(notebook_node, resources)

    return notebook_node
