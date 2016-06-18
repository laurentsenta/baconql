import logging
import os
from os import path

import click

from . import loader
from . import parser
from . import render
from .F import Chain

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)


@click.command()
@click.argument('path_in')
@click.argument('path_out')
def compiler(path_in, path_out):
    compile(path_in, path_out)


def compile_file(path_in, path_out):
    assert path.isfile(path_in), "compiling folders not supported yet"
    assert not path.isfile(path_out), "output to a folder"

    if not path.exists(path_out):
        os.makedirs(path_out)

    init = path.join(path_out, '__init__.py')
    if not path.exists(init):
        with open(init, 'w') as f:
            pass

    name_in, ext = path.splitext(path.basename(path_in))
    out = path.join(path_out, name_in + '.py')

    log.debug('rendering to %s', out)

    file = loader.load_file(path_in)
    tokens = loader.tokenize_content(file.file_path, file.content)
    parsed = parser.parse(tokens)
    render.render(out, parsed)


def compile(path_in, path_out):
    assert not path.isfile(path_out), "output to a folder"

    if path.isdir(path_in):
        files = [path.join(path_in, p) for p in os.listdir(path_in)]
    else:
        files = [path_in]

    for file in files:
        compile_file(file, path_out)
