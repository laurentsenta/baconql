import os
from os import path

import pytest

from compiler import loader, parser

__DIR = os.path.dirname(os.path.realpath(__file__))
SQL_BASIC = path.join(__DIR, 'sql', 'basic.sql')


@pytest.fixture(scope='session')
def loaded():
    return loader.load(SQL_BASIC)


@pytest.fixture(scope='session')
def parsed(loaded):
    return parser.parse(loaded)


def test_loader_count(loaded):
    assert len(loaded) == 2


def test_loader_content(loaded):
    assert loaded[0][0] == '-- count_all :? :s'
    assert loaded[1][0] == '-- insert_simple :i :n'


def test_parser_names(parsed):
    assert parsed[0].name == 'count_all'
    assert parsed[1].name == 'insert_simple'


def test_parser_basics(parsed):
    assert len(parsed[0].args) == 0
    assert len(parsed[1].args) == 1
