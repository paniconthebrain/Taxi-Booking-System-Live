# Models/PassengerModel.py
"""
Passenger Model - Represents Passengers table
"""

from datetime import datetime


class PassengerModel:
    """
    Represents a passenger in the system
    """
    
    def __init__(self, passenger_id=None, name=None, email=None, 
                 phone=None, address=None, user_id=None, created_at=None):
        """
        Initialize Passenger Model
        
        Args:
            passenger_id (int): Unique passenger identifier
            name (str): Passenger's full name
            email (str): Email address
            phone (str): Phone number
            address (str): Home address
            user_id (int): Reference to Login table
            created_at (datetime): Registration timestamp
        """
        self.passenger_id = passenger_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.user_id = user_id
        self.created_at = created_at or datetime.now()
    
    @staticmethod
    def from_db_row(row):
        """
        Create PassengerModel instance from database row
        
        Args:
            row (dict): Database row as dictionary
            
        Returns:
            PassengerModel: Passenger model instance
        """
        if not row:
            return None
        
        return PassengerModel(
            passenger_id=row.get('Passenger_ID'),
            name=row.get('Name'),
            email=row.get('Email'),
            phone=row.get('Phone'),
            address=row.get('Address'),
            user_id=row.get('User_ID'),
            created_at=row.get('Created_At')
        )
    
    def to_dict(self):
        """
        Convert model to dictionary
        
        Returns:
            dict: Passenger data as dictionary
        """
        return {
            'passenger_id': self.passenger_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'user_id': self.user_id,
            'created_at': self.created_at
        }
    
    def get_display_name(self):
        """Get formatted display name"""
        return f"{self.name} ({self.email})"
    
    def __str__(self):
        """String representation"""
        return f"Passenger(ID={self.passenger_id}, Name={self.name}, Email={self.email})"
    
    def __repr__(self):
        """Developer representation"""
        return self.__str__()