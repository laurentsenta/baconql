import os
from datetime import datetime

import click

from . import core
from . import select
from . import version


@click.group()
def migration():
    pass


def _create_file(content, path):
    with open(path, 'w') as f:
        f.write(content)


_DEFAULT_PYTHON_MIGRATION = """
from sqlalchemy import text

def up(db):
    \"\"\"executed after the sql up migration\"\"\"
    pass

def down(db):
    \"\"\"executed after the sql down migration\"\"\"
    pass
"""


@click.command()
@click.argument('name')
@click.argument('output_path')
def create(name, output_path):
    t = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    prefix = os.path.join(output_path, '%s_%s' % (t, name))

    _create_file('', prefix + '.up.sql')
    _create_file('', prefix + '.down.sql')
    _create_file(_DEFAULT_PYTHON_MIGRATION, prefix + '.py')


migration.add_command(create)


def up(db, migrations_dir):
    current_v = version.get(db)
    next_v = select.next_(migrations_dir, current_v)
    files = select.files(migrations_dir, next_v)
    core.up(db, migrations_dir, files)
    version.set(db, current_v, next_v)
    return next_v


def down(db, migrations_dir):
    current_v = version.get(db)
    next_v = select.prev_(migrations_dir, current_v)
    files = select.files(migrations_dir, current_v)
    core.down(db, migrations_dir, files)
    version.set(db, current_v, next_v)
    return next_v
