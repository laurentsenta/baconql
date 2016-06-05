from sqlalchemy import text


def up(db):
    db.execute(text("""INSERT INTO first (age) VALUES (:age);"""),
               age=51)


def down(db):
    db.execute(text("""DELETE FROM first WHERE age = :age;"""),
               age=51)
