import pytest

from baconql.compiler.defs import HEADER_INPUT, HEADER_OUTPUT, HEADER_DOC
from baconql.compiler.defs import (OP_QUERY, OP_EXECUTE, OP_RETURNING, RES_ONE,
                                   RES_AFFECTED, RES_MANY, RES_RAW, RES_SCALAR)
from baconql.compiler.exceptions import InvalidHeaderException
from baconql.compiler.parser import _without_comment_marker, _parse_def, _parse_arg


def test_trim_comment():
    assert _without_comment_marker('-- ground') == 'ground'
    assert _without_comment_marker('--control') == 'control'
    assert _without_comment_marker('  -- to') == 'to'
    assert _without_comment_marker('  -- major     ') == 'major'

    with pytest.raises(InvalidHeaderException) as e:
        _without_comment_marker('tom')
    assert "should start with `--'" in str(e)


@pytest.mark.parametrize('input, expected', [
    (":name ticking :? :1", OP_QUERY),
    (":name ticking :! :1", OP_EXECUTE),
    (":name ticking :< :1", OP_RETURNING),
    (":name away :query :1", OP_QUERY),
    (":name away :execute :1", OP_EXECUTE),
    (":name away :returning :1", OP_RETURNING)
])
def test_parse_def_op(input, expected):
    assert _parse_def(input).op == expected


@pytest.mark.parametrize('input, expected', [
    (":name the :? :1", RES_ONE),
    (":name the :! :n", RES_AFFECTED),
    (":name the :< :*", RES_MANY),
    (":name the :< :s", RES_SCALAR),
    (":name the :<", RES_RAW),

    (":name moments :? :one", RES_ONE),
    (":name moments :! :affected", RES_AFFECTED),
    (":name moments :< :many", RES_MANY),
    (":name moments :< :scalar", RES_SCALAR),
    (":name moments :< :raw", RES_RAW),
])
def test_parse_def_result(input, expected):
    assert _parse_def(input).result == expected


def test_parse_input_arg():
    p = _parse_arg(':in :arg1 : VARCHAR(40)')
    assert p.type == HEADER_INPUT
    assert p.name == 'arg1'
    assert p.value == 'VARCHAR(40)'


def test_parse_output_arg():
    p = _parse_arg(':out :arg1 : VARCHAR(40)')
    assert p.type == HEADER_OUTPUT
    assert p.name == 'arg1'
    assert p.value == 'VARCHAR(40)'


def test_parse_doc_arg():
    p = _parse_arg(':doc that make up a dull day')
    assert p.type == HEADER_DOC
    assert p.name == None
    assert p.value == 'that make up a dull day'
