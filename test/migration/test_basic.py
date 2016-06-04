import os
from os import path

import migration
from migration.utils import tables

__DIR = os.path.dirname(os.path.realpath(__file__))


def test_nothing(db):
    assert tables(db) == []


def test_one_up(db):
    migration.up(db, path.join(__DIR, 'basic'))

    assert tables(db) == ['basic']
