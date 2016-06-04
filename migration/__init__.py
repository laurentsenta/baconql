import click


@click.command()
def migration():
    click.echo("World")


def up(db, migrations_path):
    return None
