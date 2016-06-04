import itertools
import logging
import re

from . import python
from .F import Chain
from .exceptions import InvalidHeaderException, UnknownMappingException, InvalidDefinitionException

log = logging.getLogger(__name__)

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
    for (y, xs) in mapping.items():
        if value in xs:
            return y

    raise UnknownMappingException("`%s' is not a valid mapping for %s.\nValid values are: %s"
                                  % (value, mapping_name,
                                     Chain(mapping).values().flatten().join(', ').end()))


def _clean_header_str(s):
    s = s.strip()

    if not s.startswith('--'):
        raise InvalidHeaderException("header `%s' should start with `--'" % (s,))

    return s[2:].strip()


def _clean_header(line):
    try:
        return line._replace(content=_clean_header_str(line.content))
    except Exception as e:
        # TODO: Figure out a nice way to embed line information for parsing debugging.
        #       Python2 doesn't provide rethrow, this pattern kinda sucks.
        e.line_number = line.line_number
        raise e


def parse_def_str(s):
    params = Chain(s).split(' ').filter(None).end()

    if len(params) == 2:
        (name, op), ret = params, ':raw'
    elif len(params) == 3:
        name, op, ret = params
    else:
        raise InvalidDefinitionException(
                "definition `%s' is not of the form `NAME OPERATION [RETURN]'"
        )

    return Definition(name, op, ret)


def parse_def_line(line):
    try:
        return parse_def_str(line.content)
    except Exception as e:
        # TODO: Figure out a nice way to embed line information for parsing debugging.
        #       Python2 doesn't provide rethrow, this pattern kinda sucks.
        e.line_number = line.line_number
        raise e


class Definition(object):
    def __init__(self, name, str_op, str_result):
        assert python.is_valid_identifier(name), \
            "name: `%s' should be a valid python identifier" % name

        self.name = name
        self.op = _find_mapping("operation", _MAPPING_OPERATION, str_op)
        self.result = _find_mapping("result", _MAPPING_RESULT, str_result)


class Block(object):
    def __init__(self, def_, args, body):
        # TODO: test this.
        self.def_ = def_
        self.args = args
        self.body = body

    @property
    def result_template(self):
        return '_result_' + self.def_.result + '.py'

    @property
    def name(self):
        return self.def_.name

    def args_template(self, *prefix_names):
        return map(lambda name: {'name': name}, prefix_names) + self.args

    def statement(self, prefix):
        return (Chain(self.body)
                .map(lambda l: l.content)
                .join('\n' + prefix)
                .end())


def parse_arg(arg):
    m = re.match(r'^:(?P<name>\S+) : (?P<type>\S+)$', arg.content)
    assert m is not None, \
        "Invalid argument parameter `%s' at line %d" % (arg.content, arg.line_number)
    return m.groupdict()


def parse_raw_block(raw_block):
    header = (Chain(raw_block.lines)
              .call(itertools.takewhile, lambda l: l.content.startswith('--'))
              .list()
              .map(_clean_header)
              .end())
    body = raw_block.lines[len(header):]

    # Process header
    first, rest = header[0], header[1:]
    def_ = parse_def_line(first)
    args = map(parse_arg, rest)

    return Block(def_, args, body)


def parse(raw_blocks):
    return map(parse_raw_block, raw_blocks)
