import hashlib
from Db.base_db import BaseDB
from Models.UserModel import UserModel
from config import (
    ERROR_INVALID_CREDENTIALS,
    ERROR_USER_EXISTS,
    SUCCESS_REGISTRATION,
    USER_TYPE_ADMIN,
    USER_TYPE_PASSENGER,
    USER_TYPE_DRIVER
)


class UserController:
    def __init__(self):
        self.db = BaseDB()
    
    def hash_password(self, password):
        return (password)
    
    def authenticate_user(self, username, password):
        try:
            query = """
                SELECT * FROM Login 
                WHERE Username = %s AND Password = %s
            """
            row = self.db.fetch_one(query, (username, password))
            
            if row:
                return UserModel.from_db_row(row)
            return None
            
        except Exception:
            return None
    
    def create_user(self, username, password, user_type):
        try:
            if self.username_exists(username):
                return False, ERROR_USER_EXISTS, None
            
            if user_type not in [USER_TYPE_ADMIN, USER_TYPE_PASSENGER, USER_TYPE_DRIVER]:
                return False, "Invalid user type", None
            
            query = """
                INSERT INTO Login (Username, Password, User_Type)
                VALUES (%s, %s, %s)
            """
            rows = self.db.execute_query(query, (username, password, user_type))
            
            if rows > 0:
                user_id = self.db.get_last_insert_id()
                return True, SUCCESS_REGISTRATION, user_id
            else:
                return False, "Failed to create user", None
                
        except Exception:
            return False, "Error creating user", None
    
    def username_exists(self, username):
        try:
            query = "SELECT User_ID FROM Login WHERE Username = %s"
            result = self.db.fetch_one(query, (username,))
            return result is not None
        except:
            return False
    
    def get_user_by_id(self, user_id):
        try:
            query = "SELECT * FROM Login WHERE User_ID = %s"
            row = self.db.fetch_one(query, (user_id,))
            return UserModel.from_db_row(row)
        except Exception:
            return None
    
    def get_user_by_username(self, username):
        try:
            query = "SELECT * FROM Login WHERE Username = %s"
            row = self.db.fetch_one(query, (username,))
            return UserModel.from_db_row(row)
        except Exception:
            return None
    
    def get_all_users(self):
        try:
            query = "SELECT * FROM Login ORDER BY Created_At DESC"
            rows = self.db.fetch_all(query)
            return [UserModel.from_db_row(row) for row in rows]
        except Exception:
            return []
    
    def get_users_by_type(self, user_type):
        try:
            query = "SELECT * FROM Login WHERE User_Type = %s ORDER BY Created_At DESC"
            rows = self.db.fetch_all(query, (user_type,))
            return [UserModel.from_db_row(row) for row in rows]
        except Exception:
            return []
    
    def update_password(self, user_id, new_password):
        try:
            query = "UPDATE Login SET Password = %s WHERE User_ID = %s"
            rows = self.db.execute_query(query, (new_password, user_id))
            return rows > 0
        except Exception:
            return False
    
    def delete_user(self, user_id):
        try:
            query = "DELETE FROM Login WHERE User_ID = %s"
            rows = self.db.execute_query(query, (user_id,))
            return rows > 0
        except Exception:
            return False
    
    def get_total_users_count(self):
        try:
            query = "SELECT COUNT(*) as count FROM Login"
            result = self.db.fetch_one(query)
            return result['count'] if result else 0
        except:
            return 0
    
    def close(self):
        self.db.disconnect()