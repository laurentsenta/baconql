import pytest

from compiler.exceptions import InvalidHeaderException
from compiler.parser import (OP_QUERY, OP_EXECUTE, OP_INSERT, OP_RETURNING, RES_ONE,
                             RES_AFFECTED, RES_MANY, RES_RAW, RES_SCALAR)
from compiler.parser import parse_def, _clean_header_str


def test_trim_comment():
    assert _clean_header_str('-- ground') == 'ground'
    assert _clean_header_str('--control') == 'control'
    assert _clean_header_str('  -- to') == 'to'
    assert _clean_header_str('  -- major     ') == 'major'

    with pytest.raises(InvalidHeaderException) as e:
        _clean_header_str('tom')
    assert "should start with `--'" in str(e)


def test_parse_def():
    assert parse_def("ticking :? :1").op == OP_QUERY
    assert parse_def("ticking :! :1").op == OP_EXECUTE
    assert parse_def("ticking :i :1").op == OP_INSERT
    assert parse_def("ticking :< :1").op == OP_RETURNING

    assert parse_def("away :query :1").op == OP_QUERY
    assert parse_def("away :execute :1").op == OP_EXECUTE
    assert parse_def("away :insert :1").op == OP_INSERT
    assert parse_def("away :returning :1").op == OP_RETURNING

    assert parse_def("the :query :1").ret == RES_ONE
    assert parse_def("the :execute :n").ret == RES_AFFECTED
    assert parse_def("the :insert :*").ret == RES_MANY
    assert parse_def("the :returning").ret == RES_RAW
    assert parse_def("the :returning :s").ret == RES_SCALAR

    assert parse_def("moments :query :one").ret == RES_ONE
    assert parse_def("moments :execute :affected").ret == RES_AFFECTED
    assert parse_def("moments :insert :many").ret == RES_MANY
    assert parse_def("moments :returning :raw").ret == RES_RAW
    assert parse_def("moments :returning :scalar").ret == RES_SCALAR
