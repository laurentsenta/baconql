"""
Or AST, holds the structures for parsing.
"""
import re

from .F import Chain, with_defaults
from .exceptions import UnknownMappingException, InvalidHeaderException

# Query Definition
# ================

# `name operation result'
# like: `my_query :execute :scalar'
OP_QUERY = 'query'
OP_EXECUTE = 'execute'
OP_RETURNING = 'return'

RES_SCALAR = 'scalar'
RES_ONE = 'one'
RES_MANY = 'many'
RES_AFFECTED = 'affected'
RES_RAW = 'raw'

_MAPPING_OPERATION = {
    OP_QUERY: [':?', ':query'],
    OP_EXECUTE: [':!', ':execute'],
    OP_RETURNING: [':<', ':returning']
}

_MAPPING_RESULT = {
    RES_SCALAR: [':s', ':scalar'],
    RES_ONE: [':1', ':one'],
    RES_MANY: [':*', ':many'],
    RES_AFFECTED: [':n', ':affected'],
    RES_RAW: [':raw']
}


def _find_mapping(mapping_name, mapping, value):
    for y, xs in mapping.items():
        if value in xs:
            return y

    raise UnknownMappingException("`%s' is not a valid mapping for %s.\nValid values are: %s"
                                  % (value, mapping_name,
                                     Chain(mapping).values().flatten().join(', ').as_string()))


def get_operation(str_op):
    return _find_mapping("operation", _MAPPING_OPERATION, str_op)


def get_result_kind(str_result):
    return _find_mapping("result", _MAPPING_RESULT, str_result)


# Arguments
# =========

HEADER_INPUT = 'input'
HEADER_OUTPUT = 'output'
HEADER_DOC = 'doc'

HEADER_REGEXPS = {
    re.compile(r'^:(?P<name>\S+) : (?P<value>\S+)$'): HEADER_INPUT,
    re.compile(r'^>(?P<name>\S+) : (?P<value>\S+)$'): HEADER_OUTPUT,
    re.compile(r'^_doc (?P<value>.*)$'): HEADER_DOC
}


def header_type_and_content(s):
    for r, type in HEADER_REGEXPS.items():
        m = r.match(s)

        if m is not None:
            m = with_defaults(m.groupdict(), name=None, value=None)
            return type, m

    raise InvalidHeaderException("Invalid argument parameter `%s'" % s)
