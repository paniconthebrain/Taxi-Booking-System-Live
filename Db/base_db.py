# Db/base_db.py
"""
Base Database Class
Handles MySQL connection and provides utility methods for CRUD operations
"""

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG, ERROR_DB_CONNECTION


class BaseDB:
    """
    Base class for database operations
    Provides connection management and utility methods
    """
    
    def __init__(self):
        """Initialize database connection"""
        self.connection = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        """Establish connection to MySQL database"""
        try:
            # First connect without database to create it if it doesn't exist
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
            
            # Now connect to the actual database
            self.connection = mysql.connector.connect(
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                database=DB_CONFIG['database']
            )
            self.cursor = self.connection.cursor(dictionary=True)
            print(f"✓ Connected to database: {DB_CONFIG['database']}")
            
        except Error as e:
            print(f"✗ {ERROR_DB_CONNECTION}")
            print(f"  Error details: {e}")
            raise
    
    def disconnect(self):
        """Close database connection"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection and self.connection.is_connected():
                self.connection.close()
                print("✓ Database connection closed")
        except Error as e:
            print(f"✗ Error closing connection: {e}")
    
    def execute_query(self, query, params=None, fetch=False):
        """
        Execute a SQL query
        
        Args:
            query (str): SQL query to execute
            params (tuple): Parameters for the query
            fetch (bool): Whether to fetch results
            
        Returns:
            list/int: Query results or affected row count
        """
        try:
            self.cursor.execute(query, params or ())
            
            if fetch:
                return self.cursor.fetchall()
            else:
                self.connection.commit()
                return self.cursor.rowcount
                
        except Error as e:
            print(f"✗ Query execution error: {e}")
            print(f"  Query: {query[:100]}...")
            if self.connection:
                self.connection.rollback()
            return None if fetch else 0
    
    def execute_many(self, query, data_list):
        """
        Execute batch insert/update operations
        
        Args:
            query (str): SQL query with placeholders
            data_list (list): List of tuples containing data
            
        Returns:
            int: Number of affected rows
        """
        try:
            self.cursor.executemany(query, data_list)
            self.connection.commit()
            return self.cursor.rowcount
        except Error as e:
            print(f"✗ Batch execution error: {e}")
            if self.connection:
                self.connection.rollback()
            return 0
    
    def fetch_one(self, query, params=None):
        """
        Fetch a single record
        
        Args:
            query (str): SQL query
            params (tuple): Query parameters
            
        Returns:
            dict: Single record as dictionary or None
        """
        try:
            self.cursor.execute(query, params or ())
            result = self.cursor.fetchone()
            return result
        except Error as e:
            print(f"✗ Fetch one error: {e}")
            return None
    
    def fetch_all(self, query, params=None):
        """
        Fetch all records
        
        Args:
            query (str): SQL query
            params (tuple): Query parameters
            
        Returns:
            list: List of records as dictionaries
        """
        try:
            self.cursor.execute(query, params or ())
            results = self.cursor.fetchall()
            return results if results else []
        except Error as e:
            print(f"✗ Fetch all error: {e}")
            return []
    
    def get_last_insert_id(self):
        """
        Get the last inserted row ID
        
        Returns:
            int: Last insert ID
        """
        try:
            return self.cursor.lastrowid
        except:
            return None
    
    def table_exists(self, table_name):
        """
        Check if a table exists in the database
        
        Args:
            table_name (str): Name of the table to check
            
        Returns:
            bool: True if table exists, False otherwise
        """
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
        """
        Get the number of rows in a table
        
        Args:
            table_name (str): Name of the table
            
        Returns:
            int: Number of rows in the table
        """
        try:
            query = f"SELECT COUNT(*) as count FROM {table_name}"
            result = self.fetch_one(query)
            return result['count'] if result else 0
        except:
            return 0


# Test connection
if __name__ == "__main__":
    try:
        print("\n" + "="*50)
        print("Testing Database Connection...")
        print("="*50 + "\n")
        
        db = BaseDB()
        
        # Test table existence check
        print(f"Login table exists: {db.table_exists('Login')}")
        
        print("\n" + "="*50)
        print("✓ Database connection test successful!")
        print("="*50 + "\n")
        
        db.disconnect()
        
    except Exception as e:
        print(f"\n✗ Connection test failed: {e}\n")