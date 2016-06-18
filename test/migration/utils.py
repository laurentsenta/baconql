
def trim_backend_tables(tables):
    return [x for x in tables if x != 'sqlite_sequence']