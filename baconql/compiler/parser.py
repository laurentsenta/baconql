import itertools
import logging

from . import defs
from . import python
from .F import Chain
from .exceptions import InvalidHeaderException, InvalidDefinitionException

log = logging.getLogger(__name__)


class Arg(object):
    def __init__(self, type, name, value):
        self.type = type
        self.name = name
        self.value = value

    @classmethod
    def from_type(cls, t, content):
        return cls(t, content['name'], content['value'])

    @property
    def is_input(self):
        return self.type == defs.HEADER_INPUT

    @property
    def is_output(self):
        return self.type == defs.HEADER_OUTPUT

    @property
    def is_doc(self):
        return self.type == defs.HEADER_DOC


class Definition(object):
    def __init__(self, name, str_op, str_result):
        assert python.is_valid_identifier(name), \
            "name: `%s' should be a valid python identifier" % name

        self.name = name
        self.op = defs.get_operation(str_op)
        self.result = defs.get_result_kind(str_result)


class Block(object):
    def __init__(self, def_, args, body):
        # TODO: test this.
        self.def_ = def_
        self.body = body

        self.input_args = [x for x in args if x.is_input]
        self.output_args = [x for x in args if x.is_output]
        self.docs = [x for x in args if x.is_doc]

        assert sum(map(len, [self.input_args, self.output_args, self.docs])) == len(args)

    @property
    def result_template(self):
        return '_result_' + self.def_.result + '.py'

    @property
    def name(self):
        return self.def_.name

    def input_names(self, *prefix_names):
        return list(prefix_names) + [x.name for x in self.input_args]

    def statement(self, prefix):
        return (Chain(self.body)
                .join('\n' + prefix)
                .as_str())


def parse(raw_blocks):
    return map(_parse_raw_block, raw_blocks)


def _parse_raw_block(raw_block):
    header, body = _extract_header_prefix(raw_block.lines)

    first, rest = header[0], header[1:]

    def_ = _parse_def(first)
    args = list(map(_parse_arg, rest))

    return Block(def_, args, body)


def _extract_header_prefix(block_lines):
    header = (Chain(block_lines)
              .call(itertools.takewhile, lambda l: l.startswith('--'))
              .map(_without_comment_marker)
              .as_list())
    body = block_lines[len(header):]

    return header, body


def _parse_def(s):
    params = Chain(s).split(' ').filter(None).as_list()

    if len(params) == 2:
        (name, op), ret = params, ':raw'
    elif len(params) == 3:
        name, op, ret = params
    else:
        raise InvalidDefinitionException(
                "definition `%s' is not of the form `NAME OPERATION [RETURN]'"
        )

    return Definition(name, op, ret)


def _parse_arg(arg):
    t, content = defs.header_type_and_content(arg)
    return Arg.from_type(t, content)


def _without_comment_marker(s):
    """
    Remove the SQL comment marker from a string. Take care of stripping it.

    :param s:
    :return: s without `--' prefix, throw exception if no `--' is in the string
    """
    s = s.strip()

    if not s.startswith('--'):
        raise InvalidHeaderException("header `%s' should start with `--'" % (s,))

    return s[2:].lstrip()
