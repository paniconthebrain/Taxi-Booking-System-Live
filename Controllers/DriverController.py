# Controllers/DriverController.py
"""
Driver Controller - Handles driver management operations
"""

from Db.base_db import BaseDB
from Models.DriverModel import DriverModel
from config import (
    ERROR_LICENSE_EXISTS,
    ERROR_PHONE_EXISTS,
    SUCCESS_REGISTRATION,
    SUCCESS_UPDATE,
    SUCCESS_DELETE,
    DRIVER_AVAILABLE,
    DRIVER_BUSY,
    DRIVER_OFFLINE,
    validate_phone,
    validate_license
)


class DriverController:
    """
    Handles all driver-related operations
    """
    
    def __init__(self):
        """Initialize DriverController with database connection"""
        self.db = BaseDB()
    
    def create_driver(self, name, license_number, phone, email, user_id, 
                     availability=DRIVER_AVAILABLE):
        """
        Create a new driver
        
        Args:
            name (str): Driver name
            license_number (str): License number
            phone (str): Phone number
            email (str): Email address
            user_id (int): Reference to Login table
            availability (str): Initial availability status
            
        Returns:
            tuple: (success: bool, message: str, driver_id: int)
        """
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
            query = """
                INSERT INTO Drivers (Name, License_Number, Phone, Email, Availability, User_ID)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
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
        """
        Get driver by ID
        
        Args:
            driver_id (int): Driver ID
            
        Returns:
            DriverModel: Driver object or None
        """
        try:
            query = "SELECT * FROM Drivers WHERE Driver_ID = %s"
            row = self.db.fetch_one(query, (driver_id,))
            return DriverModel.from_db_row(row)
        except Exception as e:
            print(f"Get driver error: {e}")
            return None
    
    def get_driver_by_user_id(self, user_id):
        """
        Get driver by user ID
        
        Args:
            user_id (int): User ID from Login table
            
        Returns:
            DriverModel: Driver object or None
        """
        try:
            query = "SELECT * FROM Drivers WHERE User_ID = %s"
            row = self.db.fetch_one(query, (user_id,))
            return DriverModel.from_db_row(row)
        except Exception as e:
            print(f"Get driver by user ID error: {e}")
            return None
    
    def get_driver_by_license(self, license_number):
        """
        Get driver by license number
        
        Args:
            license_number (str): License number
            
        Returns:
            DriverModel: Driver object or None
        """
        try:
            query = "SELECT * FROM Drivers WHERE License_Number = %s"
            row = self.db.fetch_one(query, (license_number.upper(),))
            return DriverModel.from_db_row(row)
        except Exception as e:
            print(f"Get driver by license error: {e}")
            return None
    
    def get_all_drivers(self):
        """
        Get all drivers
        
        Returns:
            list: List of DriverModel objects
        """
        try:
            query = "SELECT * FROM Drivers ORDER BY Created_At DESC"
            rows = self.db.fetch_all(query)
            return [DriverModel.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Get all drivers error: {e}")
            return []
    
    def get_available_drivers(self):
        """
        Get all available drivers
        
        Returns:
            list: List of available DriverModel objects
        """
        try:
            query = """
                SELECT * FROM Drivers 
                WHERE Availability = %s 
                ORDER BY Name
            """
            rows = self.db.fetch_all(query, (DRIVER_AVAILABLE,))
            return [DriverModel.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Get available drivers error: {e}")
            return []
    
    def get_drivers_by_status(self, availability):
        """
        Get drivers by availability status
        
        Args:
            availability (str): Availability status
            
        Returns:
            list: List of DriverModel objects
        """
        try:
            query = "SELECT * FROM Drivers WHERE Availability = %s ORDER BY Name"
            rows = self.db.fetch_all(query, (availability,))
            return [DriverModel.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Get drivers by status error: {e}")
            return []
    
    def search_drivers(self, search_term):
        """
        Search drivers by name, license, or phone
        
        Args:
            search_term (str): Search term
            
        Returns:
            list: List of DriverModel objects
        """
        try:
            query = """
                SELECT * FROM Drivers 
                WHERE Name LIKE %s OR License_Number LIKE %s OR Phone LIKE %s
                ORDER BY Name
            """
            search_pattern = f"%{search_term}%"
            rows = self.db.fetch_all(query, (search_pattern, search_pattern, search_pattern))
            return [DriverModel.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Search drivers error: {e}")
            return []
    
    def update_driver(self, driver_id, name=None, license_number=None,
                     phone=None, email=None, availability=None):
        """
        Update driver information
        
        Args:
            driver_id (int): Driver ID
            name (str): New name (optional)
            license_number (str): New license (optional)
            phone (str): New phone (optional)
            email (str): New email (optional)
            availability (str): New availability (optional)
            
        Returns:
            tuple: (success: bool, message: str)
        """
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
            query = """
                UPDATE Drivers 
                SET Name = %s, License_Number = %s, Phone = %s, 
                    Email = %s, Availability = %s
                WHERE Driver_ID = %s
            """
            rows = self.db.execute_query(
                query, 
                (name, license_number.upper(), phone, email, availability, driver_id)
            )
            
            if rows > 0:
                return True, SUCCESS_UPDATE
            else:
                return False, "No changes made"
                
        except Exception as e:
            print(f"Update driver error: {e}")
            return False, str(e)
    
    def update_driver_availability(self, driver_id, availability):
        """
        Update driver availability status
        
        Args:
            driver_id (int): Driver ID
            availability (str): New availability status
            
        Returns:
            bool: True if successful
        """
        try:
            query = "UPDATE Drivers SET Availability = %s WHERE Driver_ID = %s"
            rows = self.db.execute_query(query, (availability, driver_id))
            return rows > 0
        except Exception as e:
            print(f"Update availability error: {e}")
            return False
    
    def delete_driver(self, driver_id):
        """
        Delete driver
        
        Args:
            driver_id (int): Driver ID
            
        Returns:
            tuple: (success: bool, message: str)
        """
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
        """
        Check if license already exists
        
        Args:
            license_number (str): License to check
            
        Returns:
            bool: True if license exists
        """
        try:
            query = "SELECT Driver_ID FROM Drivers WHERE License_Number = %s"
            result = self.db.fetch_one(query, (license_number.upper(),))
            return result is not None
        except:
            return False
    
    def phone_exists(self, phone):
        """
        Check if phone already exists
        
        Args:
            phone (str): Phone to check
            
        Returns:
            bool: True if phone exists
        """
        try:
            query = "SELECT Driver_ID FROM Drivers WHERE Phone = %s"
            result = self.db.fetch_one(query, (phone,))
            return result is not None
        except:
            return False
    
    def get_total_drivers_count(self):
        """
        Get total number of drivers
        
        Returns:
            int: Total driver count
        """
        try:
            query = "SELECT COUNT(*) as count FROM Drivers"
            result = self.db.fetch_one(query)
            return result['count'] if result else 0
        except:
            return 0
    
    def get_available_drivers_count(self):
        """
        Get count of available drivers
        
        Returns:
            int: Available driver count
        """
        try:
            query = "SELECT COUNT(*) as count FROM Drivers WHERE Availability = %s"
            result = self.db.fetch_one(query, (DRIVER_AVAILABLE,))
            return result['count'] if result else 0
        except:
            return 0
    
    def close(self):
        """Close database connection"""
        self.db.disconnect()


# Test the controller
if __name__ == "__main__":
    print("\n" + "="*60)
    print("Testing DriverController")
    print("="*60 + "\n")
    
    controller = DriverController()
    
    # Test 1: Create driver
    print("1. Creating test driver...")
    success, message, driver_id = controller.create_driver(
        "Mike Test Driver",
        "DL12345678",
        "9123456789",
        "mike@example.com",
        None,
        DRIVER_AVAILABLE
    )
    print(f"   Result: {message}, Driver ID: {driver_id}")
    
    # Test 2: Get driver
    if driver_id:
        print("\n2. Getting driver by ID...")
        driver = controller.get_driver_by_id(driver_id)
        if driver:
            print(f"   ✓ Found: {driver}")
            print(f"   Display Name: {driver.get_display_name()}")
            print(f"   Is Available: {driver.is_available()}")
        
        # Test 3: Update availability
        print("\n3. Updating driver availability to Busy...")
        success = controller.update_driver_availability(driver_id, DRIVER_BUSY)
        print(f"   Updated: {success}")
        
        # Test 4: Get available drivers
        print("\n4. Getting available drivers...")
        available = controller.get_available_drivers()
        print(f"   Available drivers: {len(available)}")
        
        # Test 5: Delete driver
        print("\n5. Deleting test driver...")
        success, message = controller.delete_driver(driver_id)
        print(f"   Result: {message}")
    
    controller.close()
    
    print("\n" + "="*60)
    print("✓ DriverController test complete")
    print("="*60 + "\n")