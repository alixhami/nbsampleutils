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
"""Utilities for exporting notebooks to markdown"""

import os
import re

from bs4 import BeautifulSoup
import nbconvert

from nbsampleutils import utils


def export_from_filepath(
    filepath, execute=False, output_dir=None, output_string_replacements=None
):
    """Utility to export a given notebook to markdown

    Args:
        filepath (string): Path to the notebook file to export to markdown
        execute (bool):
            If :data:`True`, the notebook will be executed before it is
            exported to markdown. Defaults to :data:`false`.
        output_dir (string):
            Path to the directory to output the exported markdown file
        output_string_replacements (dict(str, str), optional):
            Mapping of strings to replace in the output file
    """
    notebook_name, _ = os.path.splitext(os.path.basename(filepath))
    notebook_path, _ = os.path.split(filepath)

    if execute:
        notebook_node = utils.run_from_filepath(filepath)
    else:
        notebook_node = utils.get_notebook_from_filepath(filepath)

    if output_dir is None:
        output_dir = notebook_path

    md_name = notebook_name.replace(" ", "-").lower()

    export_from_node(
        notebook_node, md_name, output_dir, output_string_replacements)


def export_from_node(
    notebook_node, md_name, output_dir, output_string_replacements=None
):
    """Utility to export a given notebook node to markdown

    Args:
        notebook_node (nbformat.NotebookNode):
            Notebook node to convert to markdown
        md_name (string):
            Filename (without extension) for the exported markdown file
        output_dir (string):
            Path to the directory to output the exported markdown file
        output_string_replacements (dict(str, str), optional):
            Mapping of strings to replace in the output file
    """
    resources = {
        "unique_key": md_name,
        "output_files_dir": "{}-resources".format(md_name),
    }
    exporter = nbconvert.exporters.MarkdownExporter()
    output, resources = exporter.from_notebook_node(
        notebook_node, resources=resources)

    # Strip CSS styles from output because they are ignored for GitHub render
    output = strip_styles(output)

    # Make output string replacements, if any
    if output_string_replacements:
        for old_text, new_text in output_string_replacements.items():
            output = re.sub(old_text, new_text, output)

    writer = nbconvert.writers.files.FilesWriter(build_directory=output_dir)
    writer.write(output, resources, notebook_name=md_name)


def strip_styles(html):
    soup = BeautifulSoup(html, "html.parser")
    # Completely remove style tags and contents
    for tag in soup.find_all("style"):
        tag.decompose()
    # Remove all tag attributes from tables (removes dataframe styles)
    for tag in soup.find_all(["table", "tr"]):
        tag.attrs = {}
    return str(soup)
