from sqlalchemy.engine import Engine


def test_setup(db):
    assert isinstance(db, Engine)
    db.execute("SELECT * FROM typing")
    assert True
