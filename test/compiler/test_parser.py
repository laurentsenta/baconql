import pytest

from compiler.exceptions import InvalidHeaderException
from compiler.parser import (OP_QUERY, OP_EXECUTE, OP_INSERT, OP_RETURNING, RET_ONE,
                             RET_AFFECTED, RET_MANY, RET_RAW, RET_SCALAR)
from compiler.parser import parse_def, trim_comment


def test_trim_comment():
    assert trim_comment('-- ground') == 'ground'
    assert trim_comment('--control') == 'control'
    assert trim_comment('  -- to') == 'to'
    assert trim_comment('  -- major     ') == 'major'

    with pytest.raises(InvalidHeaderException) as e:
        trim_comment('tom')
    assert "should start with `--'" in str(e)


def test_parse_def():
    assert parse_def("ticking :? :1")['op'] == OP_QUERY
    assert parse_def("ticking :! :1")['op'] == OP_EXECUTE
    assert parse_def("ticking :i :1")['op'] == OP_INSERT
    assert parse_def("ticking :< :1")['op'] == OP_RETURNING

    assert parse_def("away :query :1")['op'] == OP_QUERY
    assert parse_def("away :execute :1")['op'] == OP_EXECUTE
    assert parse_def("away :insert :1")['op'] == OP_INSERT
    assert parse_def("away :returning :1")['op'] == OP_RETURNING

    assert parse_def("the :query :1")['ret'] == RET_ONE
    assert parse_def("the :execute :n")['ret'] == RET_AFFECTED
    assert parse_def("the :insert :*")['ret'] == RET_MANY
    assert parse_def("the :returning")['ret'] == RET_RAW
    assert parse_def("the :returning :s")['ret'] == RET_SCALAR

    assert parse_def("moments :query :one")['ret'] == RET_ONE
    assert parse_def("moments :execute :affected")['ret'] == RET_AFFECTED
    assert parse_def("moments :insert :many")['ret'] == RET_MANY
    assert parse_def("moments :returning :raw")['ret'] == RET_RAW
    assert parse_def("moments :returning :scalar")['ret'] == RET_SCALAR
