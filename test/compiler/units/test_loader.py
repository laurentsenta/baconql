import pytest

from baconql.compiler import loader

test_data = [
    ("test_0",
     """

     """,
     []),
    ("test_1",
     """
     -- header
     body
     """,
     [("test_1",
       [(2, '-- header'),
        (3, 'body')])
      ]),
    ("test_2",
     """
     -- header1
     body

     -- header2
     body2
     """,
     [("test_2",
       [(2, '-- header1'),
        (3, 'body')]),
      ("test_2",
       [(5, '-- header2'),
        (6, 'body2')])]),
    ("test_3",
     """
     -- header 1
     body
     -- with
     -- some
     -- comments
     body bis
     body third
     """,
     [("test_3",
       [(2, '-- header 1'),
        (3, 'body'),
        (4, '-- with'),
        (5, '-- some'),
        (6, '-- comments'),
        (7, 'body bis'),
        (8, 'body third')])])
]


@pytest.mark.parametrize("name, content, expected", test_data)
def test_tokenize(name, content, expected):
    lines = map(str.strip, content.split('\n'))
    tokenized = loader.tokenize_lines(name, lines)
    assert tokenized == expected
