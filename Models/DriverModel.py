from datetime import datetime
from config import DRIVER_AVAILABLE, DRIVER_BUSY, DRIVER_OFFLINE


class DriverModel:
    
    def __init__(self, driver_id=None, name=None, license_number=None,
                 phone=None, email=None, availability=None, 
                 user_id=None, created_at=None):

        self.driver_id = driver_id
        self.name = name
        self.license_number = license_number
        self.phone = phone
        self.email = email
        self.availability = availability or DRIVER_AVAILABLE
        self.user_id = user_id
        self.created_at = created_at or datetime.now()
    
    @staticmethod
    def from_db_row(row):

        if not row:
            return None
        
        return DriverModel(
            driver_id=row.get('Driver_ID'),
            name=row.get('Name'),
            license_number=row.get('License_Number'),
            phone=row.get('Phone'),
            email=row.get('Email'),
            availability=row.get('Availability'),
            user_id=row.get('User_ID'),
            created_at=row.get('Created_At')
        )
    
    def to_dict(self):

        return {
            'driver_id': self.driver_id,
            'name': self.name,
            'license_number': self.license_number,
            'phone': self.phone,
            'email': self.email,
            'availability': self.availability,
            'user_id': self.user_id,
            'created_at': self.created_at
        }
    
    def is_available(self):
        """Check if driver is available"""
        return self.availability == DRIVER_AVAILABLE
    
    def is_busy(self):
        """Check if driver is busy"""
        return self.availability == DRIVER_BUSY
    
    def is_offline(self):
        """Check if driver is offline"""
        return self.availability == DRIVER_OFFLINE
    
    def set_available(self):
        """Set driver as available"""
        self.availability = DRIVER_AVAILABLE
    
    def set_busy(self):
        """Set driver as busy"""
        self.availability = DRIVER_BUSY
    
    def set_offline(self):
        """Set driver as offline"""
        self.availability = DRIVER_OFFLINE
    
    def get_display_name(self):
        """Get formatted display name"""
        return f"{self.name} (License: {self.license_number})"

    def get_status_color(self):
        """Get a color representing current availability status"""
        colors = {
            DRIVER_AVAILABLE: "#27AE60",  # Green
            DRIVER_BUSY: "#E67E22",       # Orange
            DRIVER_OFFLINE: "#95A5A6",    # Gray
        }
        return colors.get(self.availability, "#95A5A6")
    
    def __str__(self):
        """String representation"""
        return f"Driver(ID={self.driver_id}, Name={self.name}, Status={self.availability})"
    
    def __repr__(self):
        """Developer representation"""
        return self.__str__()