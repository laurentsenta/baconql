import pytest

from baconql.compiler.defs import (OP_QUERY, OP_EXECUTE, OP_RETURNING, RES_ONE,
                                   RES_AFFECTED, RES_MANY, RES_RAW, RES_SCALAR)
from baconql.compiler.exceptions import InvalidHeaderException
from baconql.compiler.parser import _without_comment_marker, _parse_def


def test_trim_comment():
    assert _without_comment_marker('-- ground') == 'ground'
    assert _without_comment_marker('--control') == 'control'
    assert _without_comment_marker('  -- to') == 'to'
    assert _without_comment_marker('  -- major     ') == 'major'

    with pytest.raises(InvalidHeaderException) as e:
        _without_comment_marker('tom')
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
    assert _parse_def(input).op == expected


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
    assert _parse_def(input).result == expected
