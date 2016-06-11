import click

from compiler import compiler
from migration import migration


@click.group()
def execute():
    pass


execute.add_command(compiler)
execute.add_command(migration)

if __name__ == '__main__':
    execute()
