# Controllers/UserController.py
"""
User Controller - Handles user authentication and user management
"""

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
    """
    Handles all user-related operations including authentication
    """
    
    def __init__(self):
        """Initialize UserController with database connection"""
        self.db = BaseDB()
    
    def hash_password(self, password):
        """
        Hash password using SHA-256
        
        Args:
            password (str): Plain text password
            
        Returns:
            str: Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate_user(self, username, password):
        """
        Authenticate user with username and password
        
        Args:
            username (str): Username
            password (str): Plain text password
            
        Returns:
            UserModel: User object if authentication successful, None otherwise
        """
        try:
            hashed_password = self.hash_password(password)
            query = """
                SELECT * FROM Login 
                WHERE Username = %s AND Password = %s
            """
            row = self.db.fetch_one(query, (username, hashed_password))
            
            if row:
                return UserModel.from_db_row(row)
            return None
            
        except Exception as e:
            print(f"Authentication error: {e}")
            return None
    
    def create_user(self, username, password, user_type):
        """
        Create a new user account
        
        Args:
            username (str): Username
            password (str): Plain text password
            user_type (str): Type of user (Admin/Passenger/Driver)
            
        Returns:
            tuple: (success: bool, message: str, user_id: int)
        """
        try:
            # Check if username already exists
            if self.username_exists(username):
                return False, ERROR_USER_EXISTS, None
            
            # Validate user type
            if user_type not in [USER_TYPE_ADMIN, USER_TYPE_PASSENGER, USER_TYPE_DRIVER]:
                return False, "Invalid user type", None
            
            # Hash password and insert
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
                
        except Exception as e:
            print(f"Create user error: {e}")
            return False, str(e), None
    
    def username_exists(self, username):
        """
        Check if username already exists
        
        Args:
            username (str): Username to check
            
        Returns:
            bool: True if username exists
        """
        try:
            query = "SELECT User_ID FROM Login WHERE Username = %s"
            result = self.db.fetch_one(query, (username,))
            return result is not None
        except:
            return False
    
    def get_user_by_id(self, user_id):
        """
        Get user by ID
        
        Args:
            user_id (int): User ID
            
        Returns:
            UserModel: User object or None
        """
        try:
            query = "SELECT * FROM Login WHERE User_ID = %s"
            row = self.db.fetch_one(query, (user_id,))
            return UserModel.from_db_row(row)
        except Exception as e:
            print(f"Get user error: {e}")
            return None
    
    def get_user_by_username(self, username):
        """
        Get user by username
        
        Args:
            username (str): Username
            
        Returns:
            UserModel: User object or None
        """
        try:
            query = "SELECT * FROM Login WHERE Username = %s"
            row = self.db.fetch_one(query, (username,))
            return UserModel.from_db_row(row)
        except Exception as e:
            print(f"Get user error: {e}")
            return None
    
    def get_all_users(self):
        """
        Get all users
        
        Returns:
            list: List of UserModel objects
        """
        try:
            query = "SELECT * FROM Login ORDER BY Created_At DESC"
            rows = self.db.fetch_all(query)
            return [UserModel.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Get all users error: {e}")
            return []
    
    def get_users_by_type(self, user_type):
        """
        Get all users of a specific type
        
        Args:
            user_type (str): User type (Admin/Passenger/Driver)
            
        Returns:
            list: List of UserModel objects
        """
        try:
            query = "SELECT * FROM Login WHERE User_Type = %s ORDER BY Created_At DESC"
            rows = self.db.fetch_all(query, (user_type,))
            return [UserModel.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Get users by type error: {e}")
            return []
    
    def update_password(self, user_id, new_password):
        """
        Update user password
        
        Args:
            user_id (int): User ID
            new_password (str): New plain text password
            
        Returns:
            bool: True if successful
        """
        try:
            hashed_password = self.hash_password(new_password)
            query = "UPDATE Login SET Password = %s WHERE User_ID = %s"
            rows = self.db.execute_query(query, (hashed_password, user_id))
            return rows > 0
        except Exception as e:
            print(f"Update password error: {e}")
            return False
    
    def delete_user(self, user_id):
        """
        Delete user account
        
        Args:
            user_id (int): User ID
            
        Returns:
            bool: True if successful
        """
        try:
            query = "DELETE FROM Login WHERE User_ID = %s"
            rows = self.db.execute_query(query, (user_id,))
            return rows > 0
        except Exception as e:
            print(f"Delete user error: {e}")
            return False
    
    def get_total_users_count(self):
        """
        Get total number of users
        
        Returns:
            int: Total user count
        """
        try:
            query = "SELECT COUNT(*) as count FROM Login"
            result = self.db.fetch_one(query)
            return result['count'] if result else 0
        except:
            return 0
    
    def close(self):
        """Close database connection"""
        self.db.disconnect()


# Test the controller
if __name__ == "__main__":
    print("\n" + "="*60)
    print("Testing UserController")
    print("="*60 + "\n")
    
    controller = UserController()
    
    # Test 1: Create a test user
    print("1. Creating test user...")
    success, message, user_id = controller.create_user(
        "testuser",
        "test123",
        "Passenger"
    )
    print(f"   Result: {message}, User ID: {user_id}")
    
    # Test 2: Authenticate
    print("\n2. Authenticating user...")
    user = controller.authenticate_user("testuser", "test123")
    if user:
        print(f"   ✓ Authentication successful: {user}")
    else:
        print("   ✗ Authentication failed")
    
    # Test 3: Check username exists
    print("\n3. Checking if username exists...")
    exists = controller.username_exists("testuser")
    print(f"   Username 'testuser' exists: {exists}")
    
    # Test 4: Get all users
    print("\n4. Getting all users...")
    users = controller.get_all_users()
    print(f"   Total users: {len(users)}")
    for u in users[:3]:  # Show first 3
        print(f"   - {u}")
    
    # Clean up
    if user_id:
        print(f"\n5. Deleting test user (ID: {user_id})...")
        deleted = controller.delete_user(user_id)
        print(f"   Deleted: {deleted}")
    
    controller.close()
    
    print("\n" + "="*60)
    print("✓ UserController test complete")
    print("="*60 + "\n")