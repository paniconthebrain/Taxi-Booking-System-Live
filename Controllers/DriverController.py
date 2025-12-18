# Controllers/DriverController.py
"""Driver Controller - Handles driver management operations"""
from Db.base_db import BaseDB
from Models.DriverModel import DriverModel
from config import (ERROR_LICENSE_EXISTS,ERROR_PHONE_EXISTS,SUCCESS_REGISTRATION,SUCCESS_UPDATE,SUCCESS_DELETE,DRIVER_AVAILABLE
                    ,DRIVER_BUSY,DRIVER_OFFLINE,validate_phone,validate_license
)
class DriverController:
    """Handles all driver-related operations"""
    
    def __init__(self):
        """Initialize DriverController with database connection"""
        self.db = BaseDB()
    
    def create_driver(self, name, license_number, phone, email, user_id, 
                     availability=DRIVER_AVAILABLE):
        """ Create a new driver"""
        try:
            # Validate phone
            if not validate_phone(phone):
                return False, "Invalid phone number", None
            # Validate license
            if not validate_license(license_number):
                return False, "Invalid license number format", None
            # Check if license already exists
            if self.license_exists(license_number):
                return False, ERROR_LICENSE_EXISTS, None
            # Check if phone already exists
            if self.phone_exists(phone):
                return False, ERROR_PHONE_EXISTS, None
            # Insert driver
            query = """INSERT INTO Drivers (Name, License_Number, Phone, Email, Availability, User_ID) VALUES (%s, %s, %s, %s, %s, %s) """
            rows = self.db.execute_query(
                query, 
                (name, license_number.upper(), phone, email, availability, user_id)
            )
            if rows > 0:
                driver_id = self.db.get_last_insert_id()
                return True, SUCCESS_REGISTRATION, driver_id
            else:
                return False, "Failed to create driver", None
                
        except Exception as e:
            print(f"Create driver error: {e}")
            return False, str(e), None
    
    def get_driver_by_id(self, driver_id):
        """Get driver by ID """
        try:
            query = "SELECT * FROM Drivers WHERE Driver_ID = %s"
            row = self.db.fetch_one(query, (driver_id,))
            return DriverModel.from_db_row(row)
        except Exception as e:
            print(f"Get driver error: {e}")
            return None
    
    def get_driver_by_user_id(self, user_id):
        """ Get driver by user ID """
        try:
            query = "SELECT * FROM Drivers WHERE User_ID = %s"
            row = self.db.fetch_one(query, (user_id,))
            return DriverModel.from_db_row(row)
        except Exception as e:
            print(f"Get driver by user ID error: {e}")
            return None
    
    def get_driver_by_license(self, license_number):
        """        Get driver by license number        """
        try:
            query = "SELECT * FROM Drivers WHERE License_Number = %s"
            row = self.db.fetch_one(query, (license_number.upper(),))
            return DriverModel.from_db_row(row)
        except Exception as e:
            print(f"Get driver by license error: {e}")
            return None
    
    def get_all_drivers(self):
        """        Get all drivers                """
        try:
            query = "SELECT * FROM Drivers ORDER BY Created_At DESC"
            rows = self.db.fetch_all(query)
            return [DriverModel.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Get all drivers error: {e}")
            return []
    
    def get_available_drivers(self):
        """        Get all available drivers        """
        try:
            query = """SELECT * FROM Drivers WHERE Availability = %s ORDER BY Name"""
            rows = self.db.fetch_all(query, (DRIVER_AVAILABLE,))
            return [DriverModel.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Get available drivers error: {e}")
            return []
    
    def get_drivers_by_status(self, availability):
        """        Get drivers by availability status        """
        try:
            query = "SELECT * FROM Drivers WHERE Availability = %s ORDER BY Name"
            rows = self.db.fetch_all(query, (availability,))
            return [DriverModel.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Get drivers by status error: {e}")
            return []
    
    def search_drivers(self, search_term):
        """        Search drivers by name, license, or phone        """
        try:
            query = """ SELECT * FROM Drivers  WHERE Name LIKE %s OR License_Number LIKE %s OR Phone LIKE %s ORDER BY Name"""
            search_pattern = f"%{search_term}%"
            rows = self.db.fetch_all(query, (search_pattern, search_pattern, search_pattern))
            return [DriverModel.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Search drivers error: {e}")
            return []
    
    def update_driver(self, driver_id, name=None, license_number=None,
                     phone=None, email=None, availability=None):
        """        Update driver information        """
        try:
            # Get current driver data
            driver = self.get_driver_by_id(driver_id)
            if not driver:
                return False, "Driver not found"
            
            # Use current values if new ones not provided
            name = name or driver.name
            license_number = license_number or driver.license_number
            phone = phone or driver.phone
            email = email or driver.email
            availability = availability or driver.availability
            
            # Validate phone if changed
            if phone != driver.phone:
                if not validate_phone(phone):
                    return False, "Invalid phone number"
                if self.phone_exists(phone):
                    return False, ERROR_PHONE_EXISTS
            
            # Validate license if changed
            if license_number != driver.license_number:
                if not validate_license(license_number):
                    return False, "Invalid license number format"
                if self.license_exists(license_number):
                    return False, ERROR_LICENSE_EXISTS
            
            # Update driver
            query = """ UPDATE Drivers  SET Name = %s, License_Number = %s, Phone = %s, Email = %s, Availability = %s WHERE Driver_ID = %s """
            rows = self.db.execute_query( query,  (name, license_number.upper(), phone, email, availability, driver_id)
            )
            if rows > 0:
                return True, SUCCESS_UPDATE
            else:
                return False, "No changes made"
                
        except Exception as e:
            print(f"Update driver error: {e}")
            return False, str(e)
    
    def update_driver_availability(self, driver_id, availability):
        """Update driver availability status"""
        try:
            query = "UPDATE Drivers SET Availability = %s WHERE Driver_ID = %s"
            rows = self.db.execute_query(query, (availability, driver_id))
            return rows > 0
        except Exception as e:
            print(f"Update availability error: {e}")
            return False
    
    def delete_driver(self, driver_id):
        """Delete driver"""
        try:
            query = "DELETE FROM Drivers WHERE Driver_ID = %s"
            rows = self.db.execute_query(query, (driver_id,))
            
            if rows > 0:
                return True, SUCCESS_DELETE
            else:
                return False, "Driver not found"
                
        except Exception as e:
            print(f"Delete driver error: {e}")
            return False, str(e)
    
    def license_exists(self, license_number):
        """Check if license already exists"""
        try:
            query = "SELECT Driver_ID FROM Drivers WHERE License_Number = %s"
            result = self.db.fetch_one(query, (license_number.upper(),))
            return result is not None
        except:
            return False
    
    def phone_exists(self, phone):
        """Check if phone already exists"""
        try:
            query = "SELECT Driver_ID FROM Drivers WHERE Phone = %s"
            result = self.db.fetch_one(query, (phone,))
            return result is not None
        except:
            return False
    
    def get_total_drivers_count(self):
        """Get total number of drivers"""
        try:
            query = "SELECT COUNT(*) as count FROM Drivers"
            result = self.db.fetch_one(query)
            return result['count'] if result else 0
        except:
            return 0
    
    def get_available_drivers_count(self):
        """Get count of available drivers"""
        try:
            query = "SELECT COUNT(*) as count FROM Drivers WHERE Availability = %s"
            result = self.db.fetch_one(query, (DRIVER_AVAILABLE,))
            return result['count'] if result else 0
        except:
            return 0
    
    def close(self):
        """Close database connection"""
        self.db.disconnect()
