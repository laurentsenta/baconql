import os
from compiler import loader, Chain
from os import path

import pytest

__DIR = os.path.dirname(os.path.realpath(__file__))
SQL_BASIC = path.join(__DIR, 'sql', 'basic.sql')


@pytest.fixture(scope='session')
def loaded():
    return (Chain(SQL_BASIC)
            .call(loader.load_file)
            .call(loader.tokenize_lines, SQL_BASIC)
            .end())


def test_count(loaded):
    assert len(loaded) == 3


def test_content(loaded):
    assert loaded[0].lines[0].content == '-- count_all :? :s'
    assert loaded[1].lines[0].content == '-- insert_simple :! :n'
