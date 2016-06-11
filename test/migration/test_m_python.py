from os import path

from sqlalchemy import text

from baconql import migration
from baconql.migration.utils import tables

DIR = path.dirname(path.realpath(__file__))
MIGRATIONS = path.join(DIR, 'm_python')


def test_nothing(db):
    assert tables(db) == []


def trim_backend_tables(tables):
    return filter(lambda x: x != 'sqlite_sequence', tables)


def list_basic(db, table):
    t = text("""SELECT * FROM %s;""" % (table,))
    e = db.execute(t)
    r = map(dict, e.fetchall())
    return r


def insert(db, table, age):
    db.execute(text("""INSERT INTO %s (age) VALUES (:age);""" % (table,)),
               age=age)


def test_one_up_is_empty(db):
    migration.up(db, MIGRATIONS)
    assert list_basic(db, 'first') == []


def test_up_with_python(db):
    migration.up(db, MIGRATIONS)
    migration.up(db, MIGRATIONS)
    assert list_basic(db, 'second') == [{'id': 1, 'age': 42}]


def test_up_with_python_then_down(db):
    migration.up(db, MIGRATIONS)
    migration.up(db, MIGRATIONS)
    insert(db, 'second', 22)
    migration.down(db, MIGRATIONS)
    assert list_basic(db, 'first') == [{'id': 2, 'age': 22}]
