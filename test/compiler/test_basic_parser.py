import os
from os import path

from baconql.compiler import parser
from .test_basic_loader import loaded

__DIR = os.path.dirname(os.path.realpath(__file__))
SQL_BASIC = path.join(__DIR, 'sql', 'basic.sql')

loaded = loaded  # Force fixture "usage" for IntelliJ linting


def test_names(loaded):
    parsed = list(parser.parse(loaded))

    assert parsed[0].name == 'count_all'
    assert parsed[1].name == 'insert_simple'


def test_basics(loaded):
    parsed = list(parser.parse(loaded))

    assert len(parsed[0].input_args) == 0
    assert len(parsed[1].input_args) == 1
