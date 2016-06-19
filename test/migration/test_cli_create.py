import os

from click.testing import CliRunner

from baconql import cli


def without_underscore_prefix(x):
    """
    :param x: in the form a_b...
    :return: b...
    """
    return '_'.join(x.split('_')[1:])


def test_cli_create(cli_folder):
    runner = CliRunner()
    result = runner.invoke(cli.execute, ['migration', 'create', 'first', cli_folder])

    ls = os.listdir(cli_folder)
    suffixes = sorted(list(map(without_underscore_prefix, ls)))

    assert result.exit_code == 0
    assert len(ls) == 3
    assert suffixes == ['first.down.sql', 'first.py', 'first.up.sql']
