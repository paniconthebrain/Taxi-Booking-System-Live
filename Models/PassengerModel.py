from datetime import datetime


class PassengerModel:
    """Passenger model."""
    
    def __init__(self, passenger_id=None, name=None, email=None, 
                 phone=None, address=None, user_id=None, created_at=None):
        """Initialize passenger model."""
        self.passenger_id = passenger_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.user_id = user_id
        self.created_at = created_at or datetime.now()
    
    @staticmethod
    def from_db_row(row):
        """Create model instance from database row."""
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
        """Convert model to dictionary."""
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
        """Get formatted display name."""
        return f"{self.name} ({self.email})"
    
    def __str__(self):
        """String representation."""
        return f"Passenger(ID={self.passenger_id}, Name={self.name}, Email={self.email})"
    
    def __repr__(self):
        """Developer representation."""
        return self.__str__()