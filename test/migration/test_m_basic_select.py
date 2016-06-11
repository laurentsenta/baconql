from os import path

import pytest

from baconql.migration import select
from baconql.migration.select import InvalidMigrationException, NoMigrationFoundException

DIR = path.dirname(path.realpath(__file__))
MIGRATIONS = path.join(DIR, 'm_basic')


def test_list_migrations():
    assert select.all(MIGRATIONS) == ['migration_01', 'migration_02']


def test_next_migration_from_none():
    assert select.next_(MIGRATIONS, None) == 'migration_01'


def test_next_migration_from_first():
    assert select.next_(MIGRATIONS, 'migration_01') == 'migration_02'


def test_next_migration_from_last_fails():
    with pytest.raises(NoMigrationFoundException):
        select.next_(MIGRATIONS, 'migration_02')


def test_next_migration_from_unknown():
    with pytest.raises(InvalidMigrationException):
        select.next_(MIGRATIONS, 'migration_42')


def test_prev_migration_from_none_fails():
    with pytest.raises(NoMigrationFoundException):
        select.prev_(MIGRATIONS, None)


def test_prev_migration_from_first():
    assert select.prev_(MIGRATIONS, 'migration_01') is None


def test_prev_migration_from_second():
    assert select.prev_(MIGRATIONS, 'migration_02') == 'migration_01'


def test_prev_migration_from_unknown():
    with pytest.raises(InvalidMigrationException):
        select.prev_(MIGRATIONS, 'migration_42')
