from sqlalchemy.engine import reflection


def tables(db):
    inspector = reflection.Inspector.from_engine(db)
    return inspector.get_table_names()
