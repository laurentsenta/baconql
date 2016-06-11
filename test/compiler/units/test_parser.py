import pytest
from compiler.exceptions import InvalidHeaderException

from baconql.compiler.parser import (OP_QUERY, OP_EXECUTE, OP_RETURNING, RES_ONE,
                                     RES_AFFECTED, RES_MANY, RES_RAW, RES_SCALAR)
from baconql.compiler.parser import parse_def_str, _clean_header_str


def test_trim_comment():
    assert _clean_header_str('-- ground') == 'ground'
    assert _clean_header_str('--control') == 'control'
    assert _clean_header_str('  -- to') == 'to'
    assert _clean_header_str('  -- major     ') == 'major'

    with pytest.raises(InvalidHeaderException) as e:
        _clean_header_str('tom')
    assert "should start with `--'" in str(e)


@pytest.mark.parametrize('input, expected', [
    ("ticking :? :1", OP_QUERY),
    ("ticking :! :1", OP_EXECUTE),
    ("ticking :< :1", OP_RETURNING),
    ("away :query :1", OP_QUERY),
    ("away :execute :1", OP_EXECUTE),
    ("away :returning :1", OP_RETURNING)
])
def test_parse_def_op(input, expected):
    assert parse_def_str(input).op == expected


@pytest.mark.parametrize('input, expected', [
    ("the :? :1", RES_ONE),
    ("the :! :n", RES_AFFECTED),
    ("the :< :*", RES_MANY),
    ("the :< :s", RES_SCALAR),
    ("the :<", RES_RAW),

    ("moments :? :one", RES_ONE),
    ("moments :! :affected", RES_AFFECTED),
    ("moments :< :many", RES_MANY),
    ("moments :< :scalar", RES_SCALAR),
    ("moments :< :raw", RES_RAW),
])
def test_parse_def_result(input, expected):
    assert parse_def_str(input).result == expected
