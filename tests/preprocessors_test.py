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
"""Tests for custom nbconvert preprocessors"""

from nbsampleutils import preprocessors
from nbsampleutils import utils


def test_replace_code_input_strings_preprocessor():
    dataset_for_display = "my_display_dataset"
    notebook_node = utils.make_notebook_node(
        ['dataset_id = "{}"'.format(dataset_for_display)]
    )
    assert dataset_for_display in notebook_node.cells[0].source
    dataset_for_execution = "my_randomized_dataset02923535"
    processor = preprocessors.ReplaceCodeInputStringsPreprocessor(
        string_replacements={dataset_for_display: dataset_for_execution}
    )

    processor.preprocess(notebook_node, {})

    assert dataset_for_display not in notebook_node.cells[0].source
    assert dataset_for_execution in notebook_node.cells[0].source


def test_replace_code_input_strings_handles_no_matching_strings():
    cell_contents = 'print("nothing to replace here")'
    notebook_node = utils.make_notebook_node([cell_contents])
    processor = preprocessors.ReplaceCodeInputStringsPreprocessor(
        string_replacements={"thing_to_replace": "replacer"}
    )

    processor.preprocess(notebook_node, {})

    assert notebook_node.cells[0].source == cell_contents
