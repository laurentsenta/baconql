import itertools
import logging
import os
from os import path

import pytest
from sqlalchemy import create_engine

__DIR = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def unique_file(*dirs_then_name):
    base_dir = path.join(*dirs_then_name[:-1])
    name = dirs_then_name[-1]

    if not path.exists(base_dir):
        os.makedirs(base_dir)

    for i in itertools.count():
        p = path.join(base_dir, '%s_%05d' % (name, i))

        if not path.exists(p):
            return p


@pytest.fixture(scope='function')
def db():
    p = unique_file('out', 'test_dbs', 'test_migrations')

    log.info("Creating db: %s", p)
    db = create_engine('sqlite:///' + p)
    return db
