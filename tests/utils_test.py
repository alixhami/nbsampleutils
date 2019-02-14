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
"""Tests for notebook utilities"""
import os

from nbconvert.preprocessors.execute import CellExecutionError
import pytest

from nbsampleutils import utils


RESOURCES_DIR = os.path.join(os.path.dirname(__file__), "resources")


def test_get_returned_output_text():
    notebook_node = utils.make_notebook_node(
        ['2 + 2']
    )
    utils.run_notebook_node(notebook_node)

    output_text = utils.get_output_text(notebook_node.cells[0])

    assert "4" in output_text


def test_get_printed_output_text():
    notebook_node = utils.make_notebook_node(
        ['print("Some numbers:")\nfor num in range(6):\n\tprint(num)']
    )
    utils.run_notebook_node(notebook_node)

    output_text = utils.get_output_text(notebook_node.cells[0])

    assert "4" in output_text


def test_get_output_text_handles_no_outputs():
    notebook_node = utils.make_notebook_node(
        ['print("Some numbers:")\nfor num in range(6):\n\tprint(num)']
    )
    del notebook_node.cells[0]["outputs"]

    output_text = utils.get_output_text(notebook_node.cells[0])

    assert output_text == ""


def test_make_notebook_node():
    code_cell_contents = ['print("hello")', "2 + 2"]

    notebook_node = utils.make_notebook_node(code_cell_contents)

    got_cells = set(cell.source for cell in notebook_node.cells)
    assert set(code_cell_contents) == got_cells


def test_run_from_filepath_replaces_all_occurrences_of_input_string():
    notebook_path = os.path.join(RESOURCES_DIR, "Variables.ipynb")
    original_notebook = utils.get_notebook_from_filepath(notebook_path)
    assert sum("Pizza" in cell.source for cell in original_notebook.cells) == 2

    notebook_node = utils.run_from_filepath(
        notebook_path, input_string_replacements={"Pizza": "Cheese"}
    )

    assert sum("Pizza" in cell.source for cell in notebook_node.cells) == 0
    assert sum("Cheese" in cell.source for cell in notebook_node.cells) == 2


@pytest.mark.parametrize("cell_input", ["undefined_variable", "%%fake_magic"])
def test_run_notebook_node_disallows_errors_by_default(cell_input):
    notebook_node = utils.make_notebook_node([cell_input])

    with pytest.raises(CellExecutionError):
        utils.run_notebook_node(notebook_node)


@pytest.mark.parametrize("cell_input", ["undefined_variable", "%%fake_magic"])
def test_run_notebook_node_can_allow_errors(cell_input):
    notebook_node = utils.make_notebook_node([cell_input])

    utils.run_notebook_node(notebook_node, allow_errors=True)


def test_run_notebook_node_allows_warnings():
    cell_input = (
        "import warnings\n"
        "warnings.warn(\"deprecated\", DeprecationWarning)"
    )
    notebook_node = utils.make_notebook_node([cell_input])

    utils.run_notebook_node(notebook_node)


def test_run_notebook_node():
    notebook_node = utils.make_notebook_node(["2 + 2"])

    utils.run_notebook_node(notebook_node)

    output = notebook_node.cells[0].outputs[0]
    assert output.data["text/plain"] == "4"
