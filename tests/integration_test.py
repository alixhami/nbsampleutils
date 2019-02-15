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
"""Integration for notebook utilities"""
import os

from nbconvert.preprocessors.execute import CellExecutionError
import pytest

from nbsampleutils import preprocessors
from nbsampleutils import utils


RESOURCES_DIR = os.path.join(os.path.dirname(__file__), "resources")


def test_sample_notebook():
    notebook_filepath = os.path.join(
        RESOURCES_DIR, "Sample tested notebook.ipynb")
    string_replacements = {"YOUR-VALUE-HERE": "secret-var-for-execution"}
    notebook_node = utils.run_from_filepath(
        notebook_filepath,
        input_string_replacements=string_replacements,
    )

    assert len(notebook_node.cells) == 2
    assert "YOUR-VALUE-HERE" not in notebook_node.cells[0].source
    assert "secret-var-for-execution" in notebook_node.cells[0].source
    assert "# TEST_CELL" in notebook_node.cells[1].source

    processor = preprocessors.RemoveTaggedCellsPreprocessor(
        tag_string="# TEST_CELL"
    )
    processor.preprocess(notebook_node, {})

    assert len(notebook_node.cells) == 1
    assert "# TEST_CELL" not in notebook_node.cells[0]


def test_sample_notebook_with_failing_assert():
    notebook_filepath = os.path.join(
        RESOURCES_DIR, "Sample tested notebook.ipynb")
    string_replacements = {"YOUR-VALUE-HERE": "unexpected-value"}

    with pytest.raises(CellExecutionError):
        utils.run_from_filepath(
            notebook_filepath,
            input_string_replacements=string_replacements,
        )
