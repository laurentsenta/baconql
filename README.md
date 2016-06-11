baconql
=======

[![Build Status](https://travis-ci.org/lsenta/baconql.svg?branch=master)](https://travis-ci.org/lsenta/baconql)

[![Coverage Status](https://coveralls.io/repos/github/lsenta/baconql/badge.svg?branch=master)](https://coveralls.io/github/lsenta/baconql?branch=master)


baconql is an attempt at reconciling myself, Python and SQL.

It provides:

 - an SQL interface without ORM or weird Python DSL,
 - a simple migration system, no boilerplate needed.


### No ORM?!

Try something:
Search for `ORM bad`. Have you read any of these articles?
Then, search for `Python SQL` or `Python SQL without ORM`. ORMs, ORMs and ORMs.

baconql is an attempt at providing an ORM free library to interact with a relational
database. It doesn't do abstract stuff away, you don't have to learn a specific Python
syntax. You write SQL, you execute SQL.

- baconql is of the opinion that SQL is the right tool for the job
  when working with a relational database. Python DSLs don't count.
- baconql uses simple conventions in your SQL files to define (at compile time)
  database functions in your Python module,
  creating a clean separation of Python and SQL code.
- _(this is stolen from HugSQL, see the notes below)_

It provides:

## Compiler

Turns .sql files into python functions.

You write a `users.sql` file:

```
-- count_all :? :s
SELECT COUNT(*)
FROM users;

-- list_all :? :*
SELECT *
FROM users;
```

It's a regular SQL file, your editor already knows how to handle it and autocomplete it
for you.

baconql generates a `users.py` file that you can import and `assert user.count_all(db) == 42`.

The exact syntax will be describe later, but basically:

- one file = one module
- one block = description header + SQL body
- description header = name + type of operation (query, mutation, returning) + cardinality of the result (one, many, scalar, affected)

That's it.


## Migration manager

that makes writing SQL migrations easiers to write and to track.

WIP.

## Notes

If you find a clever idea, it's probably a ripoff of [HugSQL](http://www.hugsql.org/),
silly stuffs are mine.

baconql relies on SQLAlchemy, my Python is rusty and I'm no SQL expert,
so SQLAlchemy provides the basics to interact with the database.
I'd love to replace it with a more focused library. Handling typing seem's to be the tricky part.

If you dig into the internals you'll see that it's more of a quick & dirty POC than a well
thought codebase. Comments & issues, good or bad, will be highly appreciated.

## Release

- requires `pypandoc` package to convert this Markdown to reStructuredText.

## TODOs

- [ ] Setup tox and make this 2.6 & 3.. compatible
- [ ] Set a license
- [ ] Shorten this readme, add usage documentation and a demo,
- [ ] Find a solution to avoid repeating every argument type
    - parse the sql to figure out the inputs?
    - allow user to provide default input/output mappings, used when doing `SELECT *' for example.
- [ ] Add option to specify a docstring and prefixes (special imports) for a module
- [ ] Clean parsing phase, maybe with a real grammar (?),
- [ ] Exceptions system with a consistent way to raise with line numbers,
- [ ] More unit-testing,
- [x] Pypi-ize,
- [ ] Split into 2 different projects.