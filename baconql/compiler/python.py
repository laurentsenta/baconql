import keyword
import re


def is_valid_identifier(s):
    # TODO: use Python3 `.isidentifier()' when possible
    # http://stackoverflow.com/a/15570599
    return (re.match(r"^[_A-Za-z][_a-zA-Z0-9]*$", s) and
            not keyword.iskeyword(s))
