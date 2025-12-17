import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG


class BaseDB:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        try:
            temp_connection = mysql.connector.connect(
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password']
            )
            temp_cursor = temp_connection.cursor()
            temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
            temp_cursor.close()
            temp_connection.close()
            
            self.connection = mysql.connector.connect(
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                database=DB_CONFIG['database']
            )
            self.cursor = self.connection.cursor(dictionary=True)
            
        except Error as e:
            raise Exception(f"Database connection error: {e}")
    
    def disconnect(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection and self.connection.is_connected():
                self.connection.close()
        except Error:
            pass
    
    def execute_query(self, query, params=None, fetch=False):
        try:
            self.cursor.execute(query, params or ())
            
            if fetch:
                return self.cursor.fetchall()
            else:
                self.connection.commit()
                return self.cursor.rowcount
                
        except Error:
            if self.connection:
                self.connection.rollback()
            return None if fetch else 0
    
    def execute_many(self, query, data_list):
        try:
            self.cursor.executemany(query, data_list)
            self.connection.commit()
            return self.cursor.rowcount
        except Error:
            if self.connection:
                self.connection.rollback()
            return 0
    
    def fetch_one(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone()
        except Error:
            return None
    
    def fetch_all(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            results = self.cursor.fetchall()
            return results if results else []
        except Error:
            return []
    
    def get_last_insert_id(self):
        try:
            return self.cursor.lastrowid
        except:
            return None
    
    def table_exists(self, table_name):
        try:
            query = """
                SELECT COUNT(*) as count
                FROM information_schema.tables
                WHERE table_schema = %s AND table_name = %s
            """
            result = self.fetch_one(query, (DB_CONFIG['database'], table_name))
            return result and result['count'] > 0
        except:
            return False
    
    def get_table_row_count(self, table_name):
        try:
            query = f"SELECT COUNT(*) as count FROM {table_name}"
            result = self.fetch_one(query)
            return result['count'] if result else 0
        except:
            return 0