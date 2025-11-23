# Db/base_db.py
from Db.DatabaseCRUD import Database

class BaseDB:
    def __init__(self):
        self.db = Database()        # Uses your MySQL connection
        self.conn = self.db.conn
        self.cursor = self.db.cursor

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()
