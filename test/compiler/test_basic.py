from sqlalchemy.engine import Engine


def test_setup(db):
    assert isinstance(db, Engine)
    db.execute("SELECT * FROM basic")
    assert True


def test_first_example(db, basic_module):
    assert basic_module.count_all(db) == 0


def test_insert(db, basic_module):
    basic_module.insert_simple(db, "albert")
    assert basic_module.count_all(db) == 1
