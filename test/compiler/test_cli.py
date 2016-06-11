import os

from click.testing import CliRunner

from baconql import cli


def contains_files(path, *files):
    assert files in os.listdir(path)


def test_cli_single_file(cli_folder):
    runner = CliRunner()
    result = runner.invoke(cli.execute, ['compiler', 'test/compiler/sql/basic.sql', cli_folder])

    assert result.exit_code == 0
    assert 'basic.py' in os.listdir(cli_folder)


def test_cli_folder(cli_folder):
    runner = CliRunner()
    result = runner.invoke(cli.execute, ['compiler', 'test/compiler/sql/', cli_folder])

    assert result.exit_code == 0
    assert 'basic.py' in os.listdir(cli_folder) and 'typing.py' in os.listdir(cli_folder)
