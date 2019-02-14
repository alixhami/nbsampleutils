# Copyright 2019 Alix Hamilton
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Custom nbconvert preprocessors"""

from nbconvert.preprocessors import Preprocessor


class ReplaceCodeInputStringsPreprocessor(Preprocessor):
    """Preprocessor to replace given strings in code inputs in a notebook"""

    def __init__(self, string_replacements=None):
        self.string_replacements = string_replacements or {}
        super().__init__()

    def preprocess_cell(self, cell, resources, index):
        if cell.cell_type == "code":
            for old_value, new_value in self.string_replacements.items():
                cell.source = cell.source.replace(old_value, new_value)
        return cell, resources
