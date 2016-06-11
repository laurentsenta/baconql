from os import path

from baconql import migration
from baconql.migration.utils import tables
from baconql.migration.version import VERSION_TABLE

DIR = path.dirname(path.realpath(__file__))
MIGRATIONS = path.join(DIR, 'm_basic')


def test_nothing(db):
    assert tables(db) == []


def trim_backend_tables(tables):
    return filter(lambda x: x != 'sqlite_sequence', tables)


def test_one_up(db):
    migration.up(db, MIGRATIONS)
    assert trim_backend_tables(tables(db)) == [VERSION_TABLE, 'first']


def test_two_ups(db):
    migration.up(db, MIGRATIONS)
    migration.up(db, MIGRATIONS)
    assert trim_backend_tables(tables(db)) == [VERSION_TABLE, 'first', 'second']


def test_up_and_down(db):
    migration.up(db, MIGRATIONS)
    migration.down(db, MIGRATIONS)
    assert trim_backend_tables(tables(db)) == [VERSION_TABLE]


def test_up_up_and_down(db):
    migration.up(db, MIGRATIONS)
    migration.up(db, MIGRATIONS)
    migration.down(db, MIGRATIONS)
    assert trim_backend_tables(tables(db)) == [VERSION_TABLE, 'first']
