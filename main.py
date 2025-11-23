import tkinter as tk
from Db.DatabaseCRUD import Database

class Main:
    def __init__(self):
        super().__init__()

        self.db = Database()
        self.db.table_create()


if __name__ == "__main__":
    app = Main()
