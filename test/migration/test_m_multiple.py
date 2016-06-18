from os import path

from baconql import migration
from baconql.migration.utils import tables
from baconql.migration.version import VERSION_TABLE
from .utils import trim_backend_tables

DIR = path.dirname(path.realpath(__file__))
MIGRATIONS = path.join(DIR, 'm_multiple')


def test_nothing(db):
    assert tables(db) == []


def test_up_multiple_operations(db):
    migration.up(db, MIGRATIONS)
    assert trim_backend_tables(tables(db)) == [VERSION_TABLE, 'one', 'two']


def test_up_and_down_multiple_operations(db):
    migration.up(db, MIGRATIONS)
    migration.down(db, MIGRATIONS)
    assert trim_backend_tables(tables(db)) == [VERSION_TABLE]
