import os
from os import path

import pytest

from baconql.compiler import loader

__DIR = os.path.dirname(os.path.realpath(__file__))
SQL_BASIC = path.join(__DIR, 'sql', 'basic.sql')


@pytest.fixture(scope='session')
def loaded():
    file = loader.load_file(SQL_BASIC)
    tokens = loader.tokenize_content(file.file_path, file.content)
    return list(tokens)


def test_count(loaded):
    assert len(loaded) == 3


def test_content(loaded):
    assert loaded[0].lines[0] == '-- count_all :? :s'
    assert loaded[1].lines[0] == '-- insert_simple :! :n'
