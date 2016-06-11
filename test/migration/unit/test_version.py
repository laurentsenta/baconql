import pytest

from baconql.migration import version
from ..conftest import db

db = db


def test_no_version(db):
    assert version.get(db) == None


def test_set_version(db):
    version.set(db, None, 'some_version')
    assert version.get(db) == 'some_version'


def test_upgrade_version(db):
    version.set(db, None, 'some_version')
    version.set(db, 'some_version', 'another_version')
    assert version.get(db) == 'another_version'


def test_upgrade_version_none_fails(db):
    with pytest.raises(Exception):
        version.set('current', 'second')
    assert version.get(db) is None


def test_upgrade_version_invalid_fails(db):
    version.set(db, None, 'first')

    with pytest.raises(Exception) as e:
        version.set(db, 'second', 'third')
    assert version.get(db) == 'first'
