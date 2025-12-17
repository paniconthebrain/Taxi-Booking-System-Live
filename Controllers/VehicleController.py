# Controllers/VehicleController.py
"""
Vehicle Controller - Handles vehicle management operations
"""

from Db.base_db import BaseDB
from Models.VehicleModel import VehicleModel
from config import (
    SUCCESS_REGISTRATION,
    SUCCESS_UPDATE,
    SUCCESS_DELETE,
    VEHICLE_TYPES,
    validate_license_plate
)


class VehicleController:
    def __init__(self):
        """Initialize VehicleController with database connection"""
        self.db = BaseDB()
    
    def create_vehicle(self, model, license_plate, vehicle_type, 
                      color=None, year=None, driver_id=None):
        """
        Create a new vehicle
        
        Args:
            model (str): Vehicle model/make
            license_plate (str): License plate number
            vehicle_type (str): Type of vehicle
            color (str): Vehicle color (optional)
            year (int): Manufacturing year (optional)
            driver_id (int): Assigned driver ID (optional)
            
        Returns:
            tuple: (success: bool, message: str, vehicle_id: int)
        """
        try:
            # Validate license plate
            if not validate_license_plate(license_plate):
                return False, "Invalid license plate format", None
            
            # Validate vehicle type
            if vehicle_type not in VEHICLE_TYPES:
                return False, f"Invalid vehicle type. Must be one of: {', '.join(VEHICLE_TYPES)}", None
            
            # Check if license plate already exists
            if self.license_plate_exists(license_plate):
                return False, "License plate already exists", None
            
            # Check if driver already has a vehicle
            if driver_id and self.driver_has_vehicle(driver_id):
                return False, "Driver already has an assigned vehicle", None
            
            # Insert vehicle
            query = """
                INSERT INTO Vehicles (Model, License_Plate, Vehicle_Type, Color, Year, Driver_ID)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            rows = self.db.execute_query(
                query,
                (model, license_plate.upper(), vehicle_type, color, year, driver_id)
            )
            
            if rows > 0:
                vehicle_id = self.db.get_last_insert_id()
                return True, SUCCESS_REGISTRATION, vehicle_id
            else:
                return False, "Failed to create vehicle", None
                
        except Exception as e:
            print(f"Create vehicle error: {e}")
            return False, str(e), None
    
    def get_vehicle_by_id(self, vehicle_id):
        """
        Get vehicle by ID
        
        Args:
            vehicle_id (int): Vehicle ID
            
        Returns:
            VehicleModel: Vehicle object or None
        """
        try:
            query = "SELECT * FROM Vehicles WHERE Vehicle_ID = %s"
            row = self.db.fetch_one(query, (vehicle_id,))
            return VehicleModel.from_db_row(row)
        except Exception as e:
            print(f"Get vehicle error: {e}")
            return None
    
    def get_vehicle_by_driver(self, driver_id):
        """
        Get vehicle assigned to a driver
        
        Args:
            driver_id (int): Driver ID
            
        Returns:
            VehicleModel: Vehicle object or None
        """
        try:
            query = "SELECT * FROM Vehicles WHERE Driver_ID = %s"
            row = self.db.fetch_one(query, (driver_id,))
            return VehicleModel.from_db_row(row)
        except Exception as e:
            print(f"Get vehicle by driver error: {e}")
            return None
    
    def get_vehicle_by_license_plate(self, license_plate):
        """
        Get vehicle by license plate
        
        Args:
            license_plate (str): License plate number
            
        Returns:
            VehicleModel: Vehicle object or None
        """
        try:
            query = "SELECT * FROM Vehicles WHERE License_Plate = %s"
            row = self.db.fetch_one(query, (license_plate.upper(),))
            return VehicleModel.from_db_row(row)
        except Exception as e:
            print(f"Get vehicle by license plate error: {e}")
            return None
    
    def get_all_vehicles(self):
        """
        Get all vehicles
        
        Returns:
            list: List of VehicleModel objects
        """
        try:
            query = "SELECT * FROM Vehicles ORDER BY Created_At DESC"
            rows = self.db.fetch_all(query)
            return [VehicleModel.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Get all vehicles error: {e}")
            return []
    
    def get_vehicles_by_type(self, vehicle_type):
        """
        Get vehicles by type
        
        Args:
            vehicle_type (str): Vehicle type
            
        Returns:
            list: List of VehicleModel objects
        """
        try:
            query = "SELECT * FROM Vehicles WHERE Vehicle_Type = %s ORDER BY Model"
            rows = self.db.fetch_all(query, (vehicle_type,))
            return [VehicleModel.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Get vehicles by type error: {e}")
            return []
    
    def get_unassigned_vehicles(self):
        """
        Get vehicles without assigned drivers
        
        Returns:
            list: List of VehicleModel objects
        """
        try:
            query = "SELECT * FROM Vehicles WHERE Driver_ID IS NULL ORDER BY Model"
            rows = self.db.fetch_all(query)
            return [VehicleModel.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Get unassigned vehicles error: {e}")
            return []
    
    def get_assigned_vehicles(self):
        """
        Get vehicles with assigned drivers
        
        Returns:
            list: List of VehicleModel objects
        """
        try:
            query = "SELECT * FROM Vehicles WHERE Driver_ID IS NOT NULL ORDER BY Model"
            rows = self.db.fetch_all(query)
            return [VehicleModel.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Get assigned vehicles error: {e}")
            return []
    
    def search_vehicles(self, search_term):
        """
        Search vehicles by model or license plate
        
        Args:
            search_term (str): Search term
            
        Returns:
            list: List of VehicleModel objects
        """
        try:
            query = """
                SELECT * FROM Vehicles 
                WHERE Model LIKE %s OR License_Plate LIKE %s
                ORDER BY Model
            """
            search_pattern = f"%{search_term}%"
            rows = self.db.fetch_all(query, (search_pattern, search_pattern))
            return [VehicleModel.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Search vehicles error: {e}")
            return []
    
    def update_vehicle(self, vehicle_id, model=None, license_plate=None,
                      vehicle_type=None, color=None, year=None, driver_id=None):
        """
        Update vehicle information
        
        Args:
            vehicle_id (int): Vehicle ID
            model (str): New model (optional)
            license_plate (str): New license plate (optional)
            vehicle_type (str): New vehicle type (optional)
            color (str): New color (optional)
            year (int): New year (optional)
            driver_id (int): New driver ID (optional, use -1 to unassign)
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Get current vehicle data
            vehicle = self.get_vehicle_by_id(vehicle_id)
            if not vehicle:
                return False, "Vehicle not found"
            
            # Use current values if new ones not provided
            model = model or vehicle.model
            license_plate = license_plate or vehicle.license_plate
            vehicle_type = vehicle_type or vehicle.vehicle_type
            color = color or vehicle.color
            year = year or vehicle.year
            
            # Handle driver_id: -1 means unassign, None means keep current
            if driver_id == -1:
                driver_id = None
            elif driver_id is None:
                driver_id = vehicle.driver_id
            
            # Validate license plate if changed
            if license_plate != vehicle.license_plate:
                if not validate_license_plate(license_plate):
                    return False, "Invalid license plate format"
                if self.license_plate_exists(license_plate):
                    return False, "License plate already exists"
            
            # Validate vehicle type
            if vehicle_type not in VEHICLE_TYPES:
                return False, f"Invalid vehicle type"
            
            # Check if new driver already has a vehicle
            if driver_id and driver_id != vehicle.driver_id:
                if self.driver_has_vehicle(driver_id):
                    return False, "Driver already has an assigned vehicle"
            
            # Update vehicle
            query = """
                UPDATE Vehicles 
                SET Model = %s, License_Plate = %s, Vehicle_Type = %s, 
                    Color = %s, Year = %s, Driver_ID = %s
                WHERE Vehicle_ID = %s
            """
            rows = self.db.execute_query(
                query,
                (model, license_plate.upper(), vehicle_type, color, year, driver_id, vehicle_id)
            )
            
            if rows > 0:
                return True, SUCCESS_UPDATE
            else:
                return False, "No changes made"
                
        except Exception as e:
            print(f"Update vehicle error: {e}")
            return False, str(e)
    
    def assign_driver(self, vehicle_id, driver_id):
        """
        Assign a driver to a vehicle
        
        Args:
            vehicle_id (int): Vehicle ID
            driver_id (int): Driver ID
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Check if driver already has a vehicle
            if self.driver_has_vehicle(driver_id):
                return False, "Driver already has an assigned vehicle"
            
            query = "UPDATE Vehicles SET Driver_ID = %s WHERE Vehicle_ID = %s"
            rows = self.db.execute_query(query, (driver_id, vehicle_id))
            
            if rows > 0:
                return True, "Driver assigned successfully"
            else:
                return False, "Vehicle not found"
                
        except Exception as e:
            print(f"Assign driver error: {e}")
            return False, str(e)
    
    def unassign_driver(self, vehicle_id):
        """
        Remove driver assignment from a vehicle
        
        Args:
            vehicle_id (int): Vehicle ID
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            query = "UPDATE Vehicles SET Driver_ID = NULL WHERE Vehicle_ID = %s"
            rows = self.db.execute_query(query, (vehicle_id,))
            
            if rows > 0:
                return True, "Driver unassigned successfully"
            else:
                return False, "Vehicle not found"
                
        except Exception as e:
            print(f"Unassign driver error: {e}")
            return False, str(e)
    
    def delete_vehicle(self, vehicle_id):
        """
        Delete vehicle
        
        Args:
            vehicle_id (int): Vehicle ID
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            query = "DELETE FROM Vehicles WHERE Vehicle_ID = %s"
            rows = self.db.execute_query(query, (vehicle_id,))
            
            if rows > 0:
                return True, SUCCESS_DELETE
            else:
                return False, "Vehicle not found"
                
        except Exception as e:
            print(f"Delete vehicle error: {e}")
            return False, str(e)
    
    def license_plate_exists(self, license_plate):
        """
        Check if license plate already exists
        
        Args:
            license_plate (str): License plate to check
            
        Returns:
            bool: True if exists
        """
        try:
            query = "SELECT Vehicle_ID FROM Vehicles WHERE License_Plate = %s"
            result = self.db.fetch_one(query, (license_plate.upper(),))
            return result is not None
        except:
            return False
    
    def driver_has_vehicle(self, driver_id):
        """
        Check if driver already has an assigned vehicle
        
        Args:
            driver_id (int): Driver ID
            
        Returns:
            bool: True if driver has vehicle
        """
        try:
            query = "SELECT Vehicle_ID FROM Vehicles WHERE Driver_ID = %s"
            result = self.db.fetch_one(query, (driver_id,))
            return result is not None
        except:
            return False
    
    def get_total_vehicles_count(self):
        """
        Get total number of vehicles
        
        Returns:
            int: Total vehicle count
        """
        try:
            query = "SELECT COUNT(*) as count FROM Vehicles"
            result = self.db.fetch_one(query)
            return result['count'] if result else 0
        except:
            return 0
    
    def close(self):
        """Close database connection"""
        self.db.disconnect()

