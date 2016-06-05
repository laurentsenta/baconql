import os
from os import path

import migration
from migration.utils import tables
from migration.version import VERSION_TABLE

__DIR = os.path.dirname(os.path.realpath(__file__))


def test_nothing(db):
    assert tables(db) == []


def trim_backend_tables(tables):
    return filter(lambda x: x != 'sqlite_sequence', tables)


def test_one_up(db):
    migration.up(db, path.join(__DIR, 'basic'))
    assert trim_backend_tables(tables(db)) == [VERSION_TABLE, 'first']

def test_two_ups(db):
    migration.up(db, path.join(__DIR, 'basic'))
    migration.up(db, path.join(__DIR, 'basic'))
    assert trim_backend_tables(tables(db)) == [VERSION_TABLE, 'first', 'second']

def test_up_and_down(db):
    migration.up(db, path.join(__DIR, 'basic'))
    migration.down(db, path.join(__DIR, 'basic'))
    assert trim_backend_tables(tables(db)) == [VERSION_TABLE]

def test_up_up_and_down(db):
    migration.up(db, path.join(__DIR, 'basic'))
    migration.up(db, path.join(__DIR, 'basic'))
    migration.down(db, path.join(__DIR, 'basic'))
    assert trim_backend_tables(tables(db)) == [VERSION_TABLE, 'first']
