#!/usr/bin/env python3

import os, glob
from pytablewriter import MarkdownTableWriter

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

inputs = glob.glob('files/*.txt')

TEMPLATE_CC = '# TEMPLATE: '

for input in inputs:
    table_name = os.path.basename(input).split('.')[0].capitalize()

    with open(input, 'r') as f:
        lines = f.readlines()

    # Ignore empty files.
    if not len(lines):
        continue

    template = None

    if lines[0].startswith(TEMPLATE_CC):
        template = lines.pop(0).split(TEMPLATE_CC)[1]

    # Strip whitespace and \n from lines and filter out empty lines.
    lines = list(filter(bool, [line.strip().replace('\n', '') for line in lines]))

    # Add missing example field using detected template.
    if template:
        value_matrix = list(chunks(lines, 2))

        for idx in range(len(value_matrix)):
            value_matrix[idx].append(
                    template.strip().format(value_matrix[idx][0])
                    )
    else:
        value_matrix = list(chunks(lines, 3))

    # Surround example string with inline code backticks.
    for idx in range(len(value_matrix)):
        value_matrix[idx][2] = "`{}`".format(value_matrix[idx][2])

    md_writer = MarkdownTableWriter(
            table_name=table_name,
            headers=['op', 'desc', 'example'],
            value_matrix=value_matrix,
            )
    md_writer.write_table()
