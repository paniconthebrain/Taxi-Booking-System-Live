# Models/UserModel.py
"""
User Model - Represents Login table
Handles user authentication data
"""

from datetime import datetime
from config import USER_TYPES


class UserModel:
    """
    Represents a user in the Login table
    """
    
    def __init__(self, user_id=None, username=None, password=None, 
                 user_type=None, created_at=None):
        """
        Initialize User Model
        
        Args:
            user_id (int): Unique user identifier
            username (str): Username for login
            password (str): Hashed password
            user_type (str): Type of user (Admin/Passenger/Driver)
            created_at (datetime): Account creation timestamp
        """
        self.user_id = user_id
        self.username = username
        self.password = password
        self.user_type = user_type
        self.created_at = created_at or datetime.now()
    
    @staticmethod
    def from_db_row(row):
        """
        Create UserModel instance from database row
        
        Args:
            row (dict): Database row as dictionary
            
        Returns:
            UserModel: User model instance
        """
        if not row:
            return None
        
        return UserModel(
            user_id=row.get('User_ID'),
            username=row.get('Username'),
            password=row.get('Password'),
            user_type=row.get('User_Type'),
            created_at=row.get('Created_At')
        )
    
    def to_dict(self):
        """
        Convert model to dictionary
        
        Returns:
            dict: User data as dictionary
        """
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'user_type': self.user_type,
            'created_at': self.created_at
        }
    
    def is_admin(self):
        """Check if user is admin"""
        return self.user_type == 'Admin'
    
    def is_passenger(self):
        """Check if user is passenger"""
        return self.user_type == 'Passenger'
    
    def is_driver(self):
        """Check if user is driver"""
        return self.user_type == 'Driver'
    
    def __str__(self):
        """String representation"""
        return f"User(ID={self.user_id}, Username={self.username}, Type={self.user_type})"
    
    def __repr__(self):
        """Developer representation"""
        return self.__str__()