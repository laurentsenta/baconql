import logging
from collections import namedtuple

log = logging.getLogger(__name__)

Line = namedtuple('Line', ['line_number', 'content'])
Block = namedtuple('Block', ['file_path', 'lines'])


def load_file(fp):
    log.debug('loading file: %s', fp)

    with open(fp, 'r') as f:
        lines = f.readlines()
        lines = map(str.strip, lines)

    return lines


def tokenize_lines(file_path, lines):
    blocks = []
    current_lines = []
    previous_empty = True

    for i, l in enumerate(lines):
        if len(l) == 0:
            previous_empty = True
            continue

        if l.startswith('--') and previous_empty:
            blocks.append(Block(file_path=file_path, lines=current_lines))
            current_lines = []

        current_lines.append(Line(line_number=i + 1, content=l))
        previous_empty = False

    blocks.append(Block(file_path=file_path, lines=current_lines))

    return blocks[1:]
