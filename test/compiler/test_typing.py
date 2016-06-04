from datetime import date

from sqlalchemy.engine import Engine


def test_setup(db):
    assert isinstance(db, Engine)
    db.execute("SELECT * FROM typing")
    assert True


def test_insert_today(db, typing_module):
    today = date.today()
    typing_module.insert_simple(db, "albert", today)

    user = typing_module.get_user(db, "albert")

    assert user['username'] == "albert"
    assert user['birth'] == today
