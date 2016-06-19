from sqlalchemy.engine import Engine


def test_setup(db):
    assert isinstance(db, Engine)
    db.execute("SELECT * FROM basic")
    assert True


def test_insert_simple(db, basic_module, auto_inputs_module):
    auto_inputs_module.insert_simple(db, "username without type defined before!")
    assert basic_module.count_all(db) == 1
