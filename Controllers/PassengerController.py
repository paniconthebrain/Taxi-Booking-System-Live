from Db.base_db import BaseDB
from Models.PassengerModel import PassengerModel
from config import (
    ERROR_EMAIL_EXISTS,
    ERROR_PHONE_EXISTS,
    SUCCESS_REGISTRATION,
    SUCCESS_UPDATE,
    SUCCESS_DELETE,
    validate_email,
    validate_phone
)


class PassengerController:

    def __init__(self):
        """Initialize PassengerController with database connection"""
        self.db = BaseDB()
    
    def create_passenger(self, name, email, phone, address, user_id):
        """
        Create a new passenger
        
        Args:
            name (str): Passenger name
            email (str): Email address
            phone (str): Phone number
            address (str): Home address
            user_id (int): Reference to Login table
            
        Returns:
            tuple: (success: bool, message: str, passenger_id: int)
        """
        try:
            # Validate email
            if not validate_email(email):
                return False, "Invalid email format", None
            
            # Validate phone
            if not validate_phone(phone):
                return False, "Invalid phone number", None
            
            # Check if email already exists
            if self.email_exists(email):
                return False, ERROR_EMAIL_EXISTS, None
            
            # Check if phone already exists
            if self.phone_exists(phone):
                return False, ERROR_PHONE_EXISTS, None
            
            # Insert passenger
            query = """
                INSERT INTO Passengers (Name, Email, Phone, Address, User_ID)
                VALUES (%s, %s, %s, %s, %s)
            """
            rows = self.db.execute_query(query, (name, email, phone, address, user_id))
            
            if rows > 0:
                passenger_id = self.db.get_last_insert_id()
                return True, SUCCESS_REGISTRATION, passenger_id
            else:
                return False, "Failed to create passenger", None
                
        except Exception as e:
            print(f"Create passenger error: {e}")
            return False, str(e), None
    
    def get_passenger_by_id(self, passenger_id):
        """
        Get passenger by ID
        
        Args:
            passenger_id (int): Passenger ID
            
        Returns:
            PassengerModel: Passenger object or None
        """
        try:
            query = "SELECT * FROM Passengers WHERE Passenger_ID = %s"
            row = self.db.fetch_one(query, (passenger_id,))
            return PassengerModel.from_db_row(row)
        except Exception as e:
            print(f"Get passenger error: {e}")
            return None
    
    def get_passenger_by_user_id(self, user_id):
        """
        Get passenger by user ID
        
        Args:
            user_id (int): User ID from Login table
            
        Returns:
            PassengerModel: Passenger object or None
        """
        try:
            query = "SELECT * FROM Passengers WHERE User_ID = %s"
            row = self.db.fetch_one(query, (user_id,))
            return PassengerModel.from_db_row(row)
        except Exception as e:
            print(f"Get passenger by user ID error: {e}")
            return None
    
    def get_passenger_by_email(self, email):
        """
        Get passenger by email
        
        Args:
            email (str): Email address
            
        Returns:
            PassengerModel: Passenger object or None
        """
        try:
            query = "SELECT * FROM Passengers WHERE Email = %s"
            row = self.db.fetch_one(query, (email,))
            return PassengerModel.from_db_row(row)
        except Exception as e:
            print(f"Get passenger by email error: {e}")
            return None
    
    def get_all_passengers(self):
        """
        Get all passengers
        
        Returns:
            list: List of PassengerModel objects
        """
        try:
            query = "SELECT * FROM Passengers ORDER BY Created_At DESC"
            rows = self.db.fetch_all(query)
            return [PassengerModel.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Get all passengers error: {e}")
            return []
    
    def search_passengers(self, search_term):
        """
        Search passengers by name, email, or phone
        
        Args:
            search_term (str): Search term
            
        Returns:
            list: List of PassengerModel objects
        """
        try:
            query = """
                SELECT * FROM Passengers 
                WHERE Name LIKE %s OR Email LIKE %s OR Phone LIKE %s
                ORDER BY Name
            """
            search_pattern = f"%{search_term}%"
            rows = self.db.fetch_all(query, (search_pattern, search_pattern, search_pattern))
            return [PassengerModel.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Search passengers error: {e}")
            return []
    
    def update_passenger(self, passenger_id, name=None, email=None, 
                        phone=None, address=None):
        """
        Update passenger information
        
        Args:
            passenger_id (int): Passenger ID
            name (str): New name (optional)
            email (str): New email (optional)
            phone (str): New phone (optional)
            address (str): New address (optional)
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Get current passenger data
            passenger = self.get_passenger_by_id(passenger_id)
            if not passenger:
                return False, "Passenger not found"
            
            # Use current values if new ones not provided
            name = name or passenger.name
            email = email or passenger.email
            phone = phone or passenger.phone
            address = address or passenger.address
            
            # Validate email if changed
            if email != passenger.email:
                if not validate_email(email):
                    return False, "Invalid email format"
                if self.email_exists(email):
                    return False, ERROR_EMAIL_EXISTS
            
            # Validate phone if changed
            if phone != passenger.phone:
                if not validate_phone(phone):
                    return False, "Invalid phone number"
                if self.phone_exists(phone):
                    return False, ERROR_PHONE_EXISTS
            
            # Update passenger
            query = """
                UPDATE Passengers 
                SET Name = %s, Email = %s, Phone = %s, Address = %s
                WHERE Passenger_ID = %s
            """
            rows = self.db.execute_query(query, (name, email, phone, address, passenger_id))
            
            if rows > 0:
                return True, SUCCESS_UPDATE
            else:
                return False, "No changes made"
                
        except Exception as e:
            print(f"Update passenger error: {e}")
            return False, str(e)
    
    def delete_passenger(self, passenger_id):
        """
        Delete passenger
        
        Args:
            passenger_id (int): Passenger ID
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            query = "DELETE FROM Passengers WHERE Passenger_ID = %s"
            rows = self.db.execute_query(query, (passenger_id,))
            
            if rows > 0:
                return True, SUCCESS_DELETE
            else:
                return False, "Passenger not found"
                
        except Exception as e:
            print(f"Delete passenger error: {e}")
            return False, str(e)
    
    def email_exists(self, email):
        """
        Check if email already exists
        
        Args:
            email (str): Email to check
            
        Returns:
            bool: True if email exists
        """
        try:
            query = "SELECT Passenger_ID FROM Passengers WHERE Email = %s"
            result = self.db.fetch_one(query, (email,))
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
            query = "SELECT Passenger_ID FROM Passengers WHERE Phone = %s"
            result = self.db.fetch_one(query, (phone,))
            return result is not None
        except:
            return False
    
    def get_total_passengers_count(self):
        """
        Get total number of passengers
        
        Returns:
            int: Total passenger count
        """
        try:
            query = "SELECT COUNT(*) as count FROM Passengers"
            result = self.db.fetch_one(query)
            return result['count'] if result else 0
        except:
            return 0
    
    def close(self):
        """Close database connection"""
        self.db.disconnect()
