from os import path

from sqlalchemy import text

from test.migration.conftest import log

SUFFIX_SQL_UP = '.up.sql'
SUFFIX_SQL_DOWN = '.down.sql'

SUFFIXES = [SUFFIX_SQL_UP, SUFFIX_SQL_DOWN]


def up(db, migration_dir, files):
    assert len(files) == 2, "Migration requires up and down SQL"

    sql_up = filter(lambda x: x.endswith(SUFFIX_SQL_UP), files)[0]
    sql_up = path.join(migration_dir, sql_up)

    execute_file(db, sql_up)


def execute_file(db, fp):
    log.debug("executing sql file: `%s'", fp)
    with open(fp, 'r') as f:
        lines = f.readlines()
        txt = '\n'.join(lines)

    db.execute(text(txt))


def down(db, migration_dir, files):
    assert len(files) == 2, "Migration requires up and down SQL"

    sql_down = filter(lambda x: x.endswith(SUFFIX_SQL_DOWN), files)[0]
    sql_down = path.join(migration_dir, sql_down)

    execute_file(db, sql_down)
