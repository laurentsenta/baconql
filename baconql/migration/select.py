import logging
import os

import core

log = logging.getLogger(__name__)


class InvalidMigrationException(Exception):
    pass


def is_migration(file_name):
    return any(filter(lambda x: file_name.endswith(x), core.SUFFIXES))


def migration_name(file_name):
    for suffix in core.SUFFIXES:
        if file_name.endswith(suffix):
            return file_name[:-len(suffix)]
    raise InvalidMigrationException("the file %s doesn't looks like not a migration file")


def all(dir):
    ls = os.listdir(dir)
    ls = filter(is_migration, ls)
    names = set(map(migration_name, ls))
    # TODO: Warn if both up/down are not present.
    return sorted(names)


class NoMigrationFoundException(Exception):
    pass


def next_(dir, current):
    names = all(dir)

    try:
        if current is None:
            return names[0]

        try:
            i = names.index(current)
        except ValueError:
            raise InvalidMigrationException("Current migration `%s' couldn't be found" % (current,))

        return names[i + 1]
    except IndexError:
        raise NoMigrationFoundException()


# `_' suffix so that it looks nicer beside `next_'
def prev_(dir, current):
    names = all(dir)

    if current is None:
        raise NoMigrationFoundException()

    try:
        i = names.index(current)
    except ValueError:
        raise InvalidMigrationException("Current migration `%s' couldn't be found" % (current,))

    if i == 0:
        return None

    try:
        return names[i - 1]
    except IndexError:
        raise NoMigrationFoundException()


def files(dir, version):
    ls = os.listdir(dir)
    return filter(lambda x: x.startswith(version), ls)
