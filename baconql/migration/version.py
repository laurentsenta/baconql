from sqlalchemy import text

from baconql.migration.utils import tables

VERSION_TABLE = 'bacon_version'


def get(db):
    if VERSION_TABLE not in tables(db):
        return None
    else:
        e = db.execute(text(
                """SELECT id FROM %s LIMIT 1;""" % (VERSION_TABLE,)
        ))
        e = e.fetchone()
        return dict(e)['id']


def create_version(db, v):
    # TODO: make this atomic / look into alembic to check if they solve the issue.

    if VERSION_TABLE not in tables(db):
        db.execute(text(
                """CREATE TABLE %s (id VARCHAR(128));""" % (VERSION_TABLE,)
        ))

    db.execute(text(
            """INSERT INTO %s (id) VALUES (:id);""" % (VERSION_TABLE,)
    ), id=v)


def update_version(db, v_before, v):
    e = db.execute(text(
            """UPDATE %s SET id = :v WHERE id = :v_before;""" % (VERSION_TABLE,)
    ), v_before=v_before, v=v)

    assert e.rowcount == 1


def set(db, v_before, v):
    if v_before is None:
        create_version(db, v)
    else:
        update_version(db, v_before, v)
