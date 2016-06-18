"""
Load and tokenize a file.

Note that the tokenization is based on sqlparse.split, its behavior is somewhat
unpredictable. It depends on line breaks, whether there's a comment at the end
of the line, etc. For now, the unit-tests are the best reference for the exact
behavior.
"""

import logging
from collections import namedtuple

import sqlparse

log = logging.getLogger(__name__)

File = namedtuple('File', ['file_path', 'content'])
Block = namedtuple('Block', ['file_path', 'has_body', 'lines'])


def load_file(fp):
    log.debug('loading file: %s', fp)

    with open(fp, 'r') as f:
        content = f.read()

    return File(fp, content)


def _extract_parts(builder, lines, current=None):
    # Done, yield if there's something to yield.
    if not lines:
        if current:
            yield builder(current)
        return

    first, rest = lines[0].rstrip(), lines[1:]
    current = current or []

    # empty line, yield previous headers
    if len(first) == 0:
        if current:
            yield builder(current)
        current = []
    # else, add to current headers or finish if we're in the body
    else:
        if first.startswith('--'):
            current += [first]
        else:
            yield builder(current + [line.rstrip() for line in lines], has_body=True)
            return

    # would have used `yield from' below but py2...
    for r in _extract_parts(builder, rest, current):
        yield r


def tokenize_content(file_path, content):
    """
    Take a SQL file with multiple statements,
    returns a list of blocks.
    """
    sql_blocks = sqlparse.split(content)
    sql_blocks = filter(None, sql_blocks)

    if not sql_blocks:
        return

    def builder(content, has_body=False):
        return Block(file_path, has_body, content)

    for block in sql_blocks:
        # would have used `yield from' below but py2...
        for r in _extract_parts(builder, block.split('\n')):
            yield r
