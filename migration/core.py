from os import path

from sqlalchemy import text

from test.migration.conftest import log

SUFFIX_SQL_UP = '.up.sql'
SUFFIX_SQL_DOWN = '.down.sql'
SUFFIX_PYTHON = '.py'

SUFFIXES = [SUFFIX_SQL_UP, SUFFIX_SQL_DOWN, SUFFIX_PYTHON]


def find_suffixed(files, suffix):
    f = filter(lambda x: x.endswith(suffix), files)

    assert len(f) <= 1, "Multiple migration for the same suffix?!"
    return f[0] if len(f) == 1 else None


def up(db, migration_dir, files):
    sql_up = find_suffixed(files, SUFFIX_SQL_UP)
    python_up = find_suffixed(files, SUFFIX_PYTHON)

    if sql_up is not None:
        sql_up = path.join(migration_dir, sql_up)
        execute_sql_file(db, sql_up)
    if python_up is not None:
        python_up = path.join(migration_dir, python_up)
        execute_python_file(db, python_up, 'up')


def down(db, migration_dir, files):
    sql_down = find_suffixed(files, SUFFIX_SQL_DOWN)
    python_down = find_suffixed(files, SUFFIX_PYTHON)

    if python_down is not None:
        python_down = path.join(migration_dir, python_down)
        execute_python_file(db, python_down, 'down')
    if sql_down is not None:
        sql_down = path.join(migration_dir, sql_down)
        execute_sql_file(db, sql_down)


def execute_sql_file(db, fp):
    log.debug("executing sql file: `%s'", fp)
    with open(fp, 'r') as f:
        lines = f.readlines()
        txt = '\n'.join(lines)

    db.execute(text(txt))


def execute_python_file(db, fp, fct):
    # Only python2 for now.
    import imp
    module_name, ext = path.splitext(path.basename(fp))
    foo = imp.load_source(module_name, fp)
    getattr(foo, fct)(db)
