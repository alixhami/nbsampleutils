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
"""Tests for notebook export functions"""

from nbsampleutils import export


DF_HTML = """\
<div>
    <style scoped="">
    .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }

        .dataframe tbody tr th {
            vertical-align: top;
        }

        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
        <thead>
            <tr style="text-align: right;">
                <th></th><th>name</th><th>count</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <th>0</th><td>James</td><td>5001762</td>
            </tr>
            <tr>
                <th>1</th><td>John</td><td>4875934</td>
            </tr>
            <tr>
                <th>2</th><td>Robert</td><td>4743843</td>
            </tr>
            <tr>
                <th>3</th><td>Michael</td><td>4354622</td>
            </tr>
            <tr>
                <th>4</th><td>William</td><td>3886371</td>
            </tr>
        </tbody>
    </table>
</div>
"""


def test_strip_styles():
    # Check that all occurrences of the targeted styling are removed
    html = DF_HTML + DF_HTML
    targets = ["<style", "style=", 'border="1"']
    for target in targets:
        assert target in html

    result = export.strip_styles(html)

    for target in targets:
        assert target not in result


def test_strip_styles_with_markdown_only_input():
    markdown = "## Markdown style header"

    result = export.strip_styles(markdown)

    assert result == markdown
