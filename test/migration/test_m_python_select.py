from os import path

from baconql.migration import select

DIR = path.dirname(path.realpath(__file__))
MIGRATIONS = path.join(DIR, 'm_python')


def test_list_migrations():
    assert select.all(MIGRATIONS) == ['migration_01', 'migration_02', 'migration_03']


def test_next_with_sql_and_py():
    assert select.next_(MIGRATIONS, 'migration_01') == 'migration_02'


def test_next_with_only_py():
    assert select.next_(MIGRATIONS, 'migration_02') == 'migration_03'
