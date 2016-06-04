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


def test_list_all_empty(db, basic_module):
    assert basic_module.list_all(db) == []


def test_list_all_with_one_item(db, basic_module):
    basic_module.insert_simple(db, "albert")
    ls = basic_module.list_all(db)

    assert len(ls) == 1
    assert ls[0]['username'] == 'albert'
    assert isinstance(ls[0]['id'], int)


def test_list_all_with_two_items(db, basic_module):
    basic_module.insert_simple(db, "albert")
    basic_module.insert_simple(db, "richard")
    ls = basic_module.list_all(db)

    assert len(ls) == 2
    assert ls[0]['username'] == 'albert'
    assert ls[1]['username'] == 'richard'
    assert isinstance(ls[0]['id'], int)
    assert isinstance(ls[1]['id'], int)


def test_get_all(db, basic_module):
    basic_module.insert_simple(db, "albert")
