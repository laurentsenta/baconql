import click

from .compiler import compiler
from .migration import migration
from . import __version__ as baconql_version


@click.group()
@click.version_option(version=baconql_version)
def execute():
    pass


execute.add_command(compiler)
execute.add_command(migration)

if __name__ == '__main__':
    execute()
