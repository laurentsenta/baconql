import click
from compiler import compiler
from migration import migration


@click.group()
def cli():
    pass

cli.add_command(compiler)
cli.add_command(migration)

if __name__ == '__main__':
    cli()