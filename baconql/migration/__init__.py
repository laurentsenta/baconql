import click

from . import core
from . import select
from . import version


@click.command()
def migration():
    click.echo("World")


def up(db, migrations_dir):
    current_v = version.get(db)
    next_v = select.next_(migrations_dir, current_v)
    files = select.files(migrations_dir, next_v)
    core.up(db, migrations_dir, files)
    version.set(db, current_v, next_v)


def down(db, migrations_dir):
    current_v = version.get(db)
    next_v = select.prev_(migrations_dir, current_v)
    files = select.files(migrations_dir, current_v)
    core.down(db, migrations_dir, files)
    version.set(db, current_v, next_v)
