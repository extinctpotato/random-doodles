#!/usr/bin/env python3

import glob

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

inputs = glob.glob('files/*.txt')

TEMPLATE_CC = '# TEMPLATE: '

for input in inputs:
    print(input)
    with open(input, 'r') as f:
        lines = f.readlines()

    if not len(lines):
        continue

    template = None

    if lines[0].startswith(TEMPLATE_CC):
        template = lines.pop(0).split(TEMPLATE_CC)[1]

    lines = list(filter(bool, [line.strip().replace('\n', '') for line in lines]))

    if template:
        value_matrix = list(chunks(lines, 2))

        for idx in range(len(value_matrix)):
            value_matrix[idx].append(
                    template.strip().format(value_matrix[idx][0])
                    )
    else:
        value_matrix = chunks(lines, 3)

    print(list(value_matrix))
