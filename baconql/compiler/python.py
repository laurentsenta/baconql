import keyword
import re


def is_valid_identifier(s):
    try:
        return s.isidentifier() and not keyword.iskeyword(s)
    except AttributeError:
        return (re.match(r"^[_A-Za-z][_a-zA-Z0-9]*$", s) and
                not keyword.iskeyword(s))
