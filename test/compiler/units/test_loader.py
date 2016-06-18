from pprint import pprint

import pytest

from baconql.compiler import loader

# Test: (name, input, output)
T_0 = (
    "test_0",
    """
    """,
    []
)

T_1 = (
    "test_1",
    ('-- header\n'
     'SELECT * FROM x;'),
    [
        ("test_1", True,
         ['-- header', 'SELECT * FROM x;'])
    ]
)

T_2 = (
    "test_2",
    ('-- header1\n'
     'SELECT * FROM y;\n'
     '\n'
     '-- header2\n'
     'SELECT * FROM z;'),
    [
        ("test_2", True,
         ['-- header1', 'SELECT * FROM y;']),
        ("test_2", True,
         ['-- header2', 'SELECT * FROM z;'])
    ]
)

T_3 = (
    "test_3",
    ('-- file header\n'
     '-- file header\n'
     '\n'
     '-- header1\n'
     'SELECT * FROM y;\n'),
    [
        ("test_3", False,
         ['-- file header',
          '-- file header']),
        ("test_3", True,
         ['-- header1',
          'SELECT * FROM y;'])
    ]
)

T_4 = (
    "test_4",
    ('-- file header\n'
     '-- file header\n'
     '\n'
     '-- head1\n'
     'SELECT * FROM y;\n'
     '-- head_end\n'),
    [
        ("test_4", False,
         ["-- file header",
          "-- file header"]),
        ("test_4", True,
         ["-- head1",
          "SELECT * FROM y;"]),
        ("test_4", False,
         ["-- head_end"])
    ]
)

T_5 = (
    "test_5",
    ('-- head1\n'
     'SELECT * FROM y;\n'
     '-- head_end\n'
     '\n'
     '-- head2\n'
     'SELECT *\n'
     '-- inner comment\n'
     'FROM y;\n'
     '-- head_end\n'),
    [
        ("test_5", True,
         ["-- head1",
          "SELECT * FROM y;"]),
        ("test_5", False,
         ["-- head_end"]),
        ("test_5", True,
         ["-- head2",
          "SELECT *",
          "-- inner comment",
          "FROM y;"]),
        ("test_5", False,
         ["-- head_end"])
    ]
)

TESTS = [T_0, T_1, T_2, T_3, T_4, T_5]


@pytest.mark.parametrize("name, content, expected", TESTS)
def test_tokenize(name, content, expected):
    tokenized = loader.tokenize_content(name, content)
    tokenized = list(tokenized)
    pprint(content)
    pprint(tokenized)
    pprint(expected)
    assert tokenized == expected
