import logging
import os
from os import path

import click

import core
import loader
import parser
from F import Chain

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)


@click.command()
@click.argument('path_in')
@click.argument('path_out')
def compiler(path_in, path_out):
    compile(path_in, path_out)


def compile(path_in, path_out):
    if not path.exists(path_out):
        os.makedirs(path_out)

    init = path.join(path_out, '__init__.py')
    if not path.exists(init):
        with open(init, 'w') as f:
            pass

    out = path_out + '/basic.py'

    log.debug('rendering to %s', out)

    (Chain(path_in)
     .call(loader.load_file)
     .call(loader.tokenize_lines, path_in)
     .call(parser.parse).call(core.render, out))
