import itertools
import logging
import re

from . import python
from .F import Chain
from .exceptions import InvalidHeaderException, UnknownMappingException, InvalidDefinitionException

log = logging.getLogger(__name__)

OP_QUERY = 'query'
OP_EXECUTE = 'execute'
OP_INSERT = 'insert'
OP_RETURNING = 'return'

RET_ONE = 'one'
RET_MANY = 'many'
RET_AFFECTED = 'affected'
RET_RAW = 'raw'

_MAPPING_OP = {
    OP_QUERY: [':?', ':query'],
    OP_EXECUTE: [':!', ':execute'],
    OP_INSERT: [':i', ':insert'],
    OP_RETURNING: [':<', ':returning']
}

_MAPPING_RET = {
    RET_ONE: [':1', ':one'],
    RET_MANY: [':*', ':many'],
    RET_AFFECTED: [':n', ':affected'],
    RET_RAW: [':raw']
}


def _find_mapping(mapping_name, mapping, value):
    for (y, xs) in mapping.items():
        if value in xs:
            return y

    raise UnknownMappingException("`%s' is not a valid mapping for %s.\nValid values are: %s"
                                  % (value, mapping_name,
                                     Chain(mapping).values().flatten().join(', ').end()))


class Block(object):
    def __init__(self, name, op, ret, args, body):
        # TODO: test this.
        assert python.is_valid_identifier(name), \
            "name: `%s' should be a valid python identifier" % name

        self.name = name
        self.op = op
        self.ret = ret
        self.args = args
        self.body = body

    def args_template(self, *names):
        return map(lambda name: {'name': name}, names) + self.args

    def statement(self, prefix):
        return ('\n' + prefix).join(self.body)


def trim_comment(l):
    l = l.strip()

    if not l.startswith('--'):
        raise InvalidHeaderException("header `%s' should start with `--'" % l)

    return l[2:].strip()


def parse_def(l):
    params = Chain(l).split(' ').filter(None).end()

    if len(params) == 2:
        (name, op), ret = params, ':raw'
    elif len(params) == 3:
        name, op, ret = params
    else:
        raise InvalidDefinitionException(
                "definition `%s' is not of the form `NAME OPERATION [RETURN]'"
        )

    return dict(name=name,
                op=_find_mapping('operations', _MAPPING_OP, op),
                ret=_find_mapping('count', _MAPPING_RET, ret))


def parse_arg(arg):
    m = re.match(r'^:(?P<name>\S+) : (?P<type>\S+)$', arg)
    assert m is not None
    return m.groupdict()


def parse_block(loaded):
    header = (Chain(loaded)
              .call(itertools.takewhile, lambda x: x.startswith('--'))
              .list()
              .map(trim_comment)
              .end())

    body = loaded[len(header):]

    first, rest = header[0], header[1:]

    def_ = parse_def(first)
    args = map(parse_arg, rest)

    return Block(def_['name'], def_['op'], def_['ret'], args, body)


def parse(loaded):
    return map(parse_block, loaded)
