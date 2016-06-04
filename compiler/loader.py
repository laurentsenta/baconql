import logging

log = logging.getLogger(__name__)


def load(fp):
    with open(fp, 'r') as f:
        lines = f.readlines()
        lines = map(str.strip, lines)

    log.debug('processing file: %s, with %d lines', fp, len(lines))

    blocks = []
    current_block = []
    previous_empty = True

    for l in lines:
        if l.startswith('--') and previous_empty:
            blocks.append(current_block)
            current_block = [l]
            previous_empty = False
        elif len(l) == 0:
            previous_empty = True
        else:
            current_block.append(l)

    blocks.append(current_block)

    return blocks[1:]
