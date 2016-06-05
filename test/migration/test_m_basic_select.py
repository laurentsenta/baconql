import os

import pytest

from migration import select
from migration.select import InvalidMigrationException, NoMigrationFoundException

__DIR = os.path.dirname(os.path.realpath(__file__))

BASIC_DIR = os.path.join(__DIR, 'm_basic')


def test_list_migrations():
    assert select.all(BASIC_DIR) == ['migration_01', 'migration_02']


def test_next_migration_from_none():
    assert select.next_(BASIC_DIR, None) == 'migration_01'


def test_next_migration_from_first():
    assert select.next_(BASIC_DIR, 'migration_01') == 'migration_02'


def test_next_migration_from_last_fails():
    with pytest.raises(NoMigrationFoundException):
        select.next_(BASIC_DIR, 'migration_02')


def test_next_migration_from_unknown():
    with pytest.raises(InvalidMigrationException):
        select.next_(BASIC_DIR, 'migration_42')


def test_prev_migration_from_none_fails():
    with pytest.raises(NoMigrationFoundException):
        select.prev_(BASIC_DIR, None)


def test_prev_migration_from_first():
    assert select.prev_(BASIC_DIR, 'migration_01') is None


def test_prev_migration_from_second():
    assert select.prev_(BASIC_DIR, 'migration_02') == 'migration_01'


def test_prev_migration_from_unknown():
    with pytest.raises(InvalidMigrationException):
        select.prev_(BASIC_DIR, 'migration_42')
