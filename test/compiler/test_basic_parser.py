import os
from os import path

import pytest

from baconql.compiler import parser
from .test_basic_loader import loaded

__DIR = os.path.dirname(os.path.realpath(__file__))
SQL_BASIC = path.join(__DIR, 'sql', 'basic.sql')

loaded = loaded  # Force fixture "usage" for linting


@pytest.fixture(scope='session')
def parsed(loaded):
    return parser.parse(loaded)


def test_names(parsed):
    assert parsed[0].name == 'count_all'
    assert parsed[1].name == 'insert_simple'


def test_basics(parsed):
    assert len(parsed[0].input_args) == 0
    assert len(parsed[1].input_args) == 1
