from sqlalchemy import text


def up(db):
    db.execute(text("""INSERT INTO second (age) VALUES (:age);"""),
               age=42)


def down(db):
    db.execute(text("""DELETE FROM second WHERE age = :age;"""),
               age=42)
