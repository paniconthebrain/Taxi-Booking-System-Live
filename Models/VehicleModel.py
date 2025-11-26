# Models/VehicleModel.py
"""
Vehicle Model - Represents Vehicles table
"""

from datetime import datetime
from config import VEHICLE_SEDAN


class VehicleModel:
    """
    Represents a vehicle in the system
    """
    
    def __init__(self, vehicle_id=None, model=None, license_plate=None,
                 vehicle_type=None, color=None, year=None, 
                 driver_id=None, created_at=None):
        """
        Initialize Vehicle Model
        
        Args:
            vehicle_id (int): Unique vehicle identifier
            model (str): Vehicle model/make
            license_plate (str): Vehicle license plate number
            vehicle_type (str): Type of vehicle (Sedan/SUV/etc)
            color (str): Vehicle color
            year (int): Manufacturing year
            driver_id (int): Reference to assigned driver
            created_at (datetime): Registration timestamp
        """
        self.vehicle_id = vehicle_id
        self.model = model
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type or VEHICLE_SEDAN
        self.color = color
        self.year = year
        self.driver_id = driver_id
        self.created_at = created_at or datetime.now()
    
    @staticmethod
    def from_db_row(row):
        """
        Create VehicleModel instance from database row
        
        Args:
            row (dict): Database row as dictionary
            
        Returns:
            VehicleModel: Vehicle model instance
        """
        if not row:
            return None
        
        return VehicleModel(
            vehicle_id=row.get('Vehicle_ID'),
            model=row.get('Model'),
            license_plate=row.get('License_Plate'),
            vehicle_type=row.get('Vehicle_Type'),
            color=row.get('Color'),
            year=row.get('Year'),
            driver_id=row.get('Driver_ID'),
            created_at=row.get('Created_At')
        )
    
    def to_dict(self):
        """
        Convert model to dictionary
        
        Returns:
            dict: Vehicle data as dictionary
        """
        return {
            'vehicle_id': self.vehicle_id,
            'model': self.model,
            'license_plate': self.license_plate,
            'vehicle_type': self.vehicle_type,
            'color': self.color,
            'year': self.year,
            'driver_id': self.driver_id,
            'created_at': self.created_at
        }
    
    def has_driver(self):
        """Check if vehicle has an assigned driver"""
        return self.driver_id is not None
    
    def get_display_name(self):
        """Get formatted display name"""
        return f"{self.model} ({self.license_plate})"
    
    def get_full_description(self):
        """Get full vehicle description"""
        parts = []
        if self.year:
            parts.append(str(self.year))
        if self.color:
            parts.append(self.color)
        parts.append(self.model)
        if self.vehicle_type:
            parts.append(f"- {self.vehicle_type}")
        return " ".join(parts)
    
    def get_short_description(self):
        """Get short vehicle description"""
        return f"{self.color} {self.model}" if self.color else self.model
    
    def is_assigned(self):
        """Check if vehicle is assigned to a driver"""
        return self.driver_id is not None
    
    def __str__(self):
        """String representation"""
        return f"Vehicle(ID={self.vehicle_id}, Model={self.model}, Plate={self.license_plate})"
    
    def __repr__(self):
        """Developer representation"""
        return self.__str__()