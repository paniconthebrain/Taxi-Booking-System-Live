# Controllers/BookingController.py
"""
Booking Controller - Handles booking/ride management operations
"""

from Db.base_db import BaseDB
from Models.BookingModel import BookingModel
from config import (
    SUCCESS_REGISTRATION,
    SUCCESS_UPDATE,
    SUCCESS_DELETE,
    BOOKING_STATUS_PENDING,
    BOOKING_STATUS_CONFIRMED,
    BOOKING_STATUS_IN_PROGRESS,
    BOOKING_STATUS_COMPLETED,
    BOOKING_STATUS_CANCELLED,
    calculate_fare,
    DRIVER_AVAILABLE,
    DRIVER_BUSY,
)
from datetime import datetime


class BookingController:
    """
    Handles all booking-related operations
    """
    
    def __init__(self):
        """Initialize BookingController with database connection"""
        self.db = BaseDB()
    
    def create_booking(self, passenger_id, pickup_location, destination, 
                      distance_km=None, driver_id=None):
        """
        Create a new booking
        
        Args:
            passenger_id (int): Passenger ID
            pickup_location (str): Pickup address
            destination (str): Destination address
            distance_km (float): Distance in kilometers (optional)
            driver_id (int): Assigned driver ID (optional)
            
        Returns:
            tuple: (success: bool, message: str, booking_id: int)
        """
        try:
            # Calculate fare if distance provided
            fare = calculate_fare(distance_km) if distance_km else None
            
            # Insert booking
            query = """
                INSERT INTO Bookings (Passenger_ID, Driver_ID, Pickup_Location, 
                                     Destination, Status, Fare, Distance_KM)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            rows = self.db.execute_query(
                query,
                (passenger_id, driver_id, pickup_location, destination, 
                 BOOKING_STATUS_PENDING, fare, distance_km)
            )
            
            if rows > 0:
                booking_id = self.db.get_last_insert_id()
                return True, SUCCESS_REGISTRATION, booking_id
            else:
                return False, "Failed to create booking", None
                
        except Exception as e:
            print(f"Create booking error: {e}")
            return False, str(e), None
    
    def get_booking_by_id(self, booking_id):
        """
        Get booking by ID
        
        Args:
            booking_id (int): Booking ID
            
        Returns:
            BookingModel: Booking object or None
        """
        try:
            query = "SELECT * FROM Bookings WHERE Booking_ID = %s"
            row = self.db.fetch_one(query, (booking_id,))
            return BookingModel.from_db_row(row)
        except Exception as e:
            print(f"Get booking error: {e}")
            return None
    
    def get_all_bookings(self):
        """
        Get all bookings
        
        Returns:
            list: List of BookingModel objects
        """
        try:
            query = "SELECT * FROM Bookings ORDER BY Booking_Date DESC"
            rows = self.db.fetch_all(query)
            return [BookingModel.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Get all bookings error: {e}")
            return []
    
    def get_bookings_by_passenger(self, passenger_id):
        """
        Get all bookings for a passenger
        
        Args:
            passenger_id (int): Passenger ID
            
        Returns:
            list: List of BookingModel objects
        """
        try:
            query = """
                SELECT * FROM Bookings 
                WHERE Passenger_ID = %s 
                ORDER BY Booking_Date DESC
            """
            rows = self.db.fetch_all(query, (passenger_id,))
            return [BookingModel.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Get bookings by passenger error: {e}")
            return []
    
    def get_bookings_by_driver(self, driver_id):
        """
        Get all bookings for a driver
        
        Args:
            driver_id (int): Driver ID
            
        Returns:
            list: List of BookingModel objects
        """
        try:
            query = """
                SELECT * FROM Bookings 
                WHERE Driver_ID = %s 
                ORDER BY Booking_Date DESC
            """
            rows = self.db.fetch_all(query, (driver_id,))
            return [BookingModel.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Get bookings by driver error: {e}")
            return []
    
    def get_bookings_by_status(self, status):
        """
        Get bookings by status
        
        Args:
            status (str): Booking status
            
        Returns:
            list: List of BookingModel objects
        """
        try:
            query = """
                SELECT * FROM Bookings 
                WHERE Status = %s 
                ORDER BY Booking_Date DESC
            """
            rows = self.db.fetch_all(query, (status,))
            return [BookingModel.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Get bookings by status error: {e}")
            return []
    
    def get_pending_bookings(self):
        """
        Get all pending bookings
        
        Returns:
            list: List of BookingModel objects
        """
        return self.get_bookings_by_status(BOOKING_STATUS_PENDING)
    
    def get_active_bookings(self):
        """
        Get all active bookings (Confirmed + In Progress)
        
        Returns:
            list: List of BookingModel objects
        """
        try:
            query = """
                SELECT * FROM Bookings 
                WHERE Status IN (%s, %s) 
                ORDER BY Booking_Date DESC
            """
            rows = self.db.fetch_all(query, (BOOKING_STATUS_CONFIRMED, BOOKING_STATUS_IN_PROGRESS))
            return [BookingModel.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Get active bookings error: {e}")
            return []
    
    def get_completed_bookings(self):
        """
        Get all completed bookings
        
        Returns:
            list: List of BookingModel objects
        """
        return self.get_bookings_by_status(BOOKING_STATUS_COMPLETED)
    
    def update_booking_status(self, booking_id, status):
        """
        Update booking status
        
        Args:
            booking_id (int): Booking ID
            status (str): New status
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # If completed, set completion date
            if status == BOOKING_STATUS_COMPLETED:
                query = """
                    UPDATE Bookings 
                    SET Status = %s, Completion_Date = %s 
                    WHERE Booking_ID = %s
                """
                rows = self.db.execute_query(query, (status, datetime.now(), booking_id))
            else:
                query = "UPDATE Bookings SET Status = %s WHERE Booking_ID = %s"
                rows = self.db.execute_query(query, (status, booking_id))
            
            if rows > 0:
                return True, SUCCESS_UPDATE
            else:
                return False, "Booking not found"
                
        except Exception as e:
            print(f"Update booking status error: {e}")
            return False, str(e)
    
    def assign_driver(self, booking_id, driver_id):
        """
        Assign driver to booking
        
        Args:
            booking_id (int): Booking ID
            driver_id (int): Driver ID
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # First, get current driver (if any) for this booking
            select_query = "SELECT Driver_ID FROM Bookings WHERE Booking_ID = %s"
            current_row = self.db.fetch_one(select_query, (booking_id,))
            if not current_row:
                return False, "Booking not found"

            previous_driver_id = current_row.get("Driver_ID")

            # Update booking with new driver and set status to Confirmed
            update_booking_query = """
                UPDATE Bookings 
                SET Driver_ID = %s, Status = %s 
                WHERE Booking_ID = %s
            """
            rows = self.db.execute_query(
                update_booking_query,
                (driver_id, BOOKING_STATUS_CONFIRMED, booking_id),
            )
            
            if rows > 0:
                # If there was a previous driver and it's different, set them back to Available
                if previous_driver_id and previous_driver_id != driver_id:
                    try:
                        self.db.execute_query(
                            "UPDATE Drivers SET Availability = %s WHERE Driver_ID = %s",
                            (DRIVER_AVAILABLE, previous_driver_id),
                        )
                    except Exception as e:
                        print(f"Warning: failed to set previous driver available: {e}")

                # Set the newly assigned driver to Busy
                try:
                    self.db.execute_query(
                        "UPDATE Drivers SET Availability = %s WHERE Driver_ID = %s",
                        (DRIVER_BUSY, driver_id),
                    )
                except Exception as e:
                    print(f"Warning: failed to set assigned driver busy: {e}")

                return True, "Driver assigned successfully"
            else:
                return False, "Booking not found"
                
        except Exception as e:
            print(f"Assign driver error: {e}")
            return False, str(e)
    
    def update_booking(self, booking_id, pickup_location=None, destination=None,
                      distance_km=None, fare=None, status=None, driver_id=None):
        """
        Update booking information
        
        Args:
            booking_id (int): Booking ID
            pickup_location (str): New pickup location (optional)
            destination (str): New destination (optional)
            distance_km (float): New distance (optional)
            fare (float): New fare (optional)
            status (str): New status (optional)
            driver_id (int): New driver ID (optional)
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Get current booking
            booking = self.get_booking_by_id(booking_id)
            if not booking:
                return False, "Booking not found"
            
            # Use current values if new ones not provided
            pickup_location = pickup_location or booking.pickup_location
            destination = destination or booking.destination
            distance_km = distance_km if distance_km is not None else booking.distance_km
            fare = fare if fare is not None else booking.fare
            status = status or booking.status
            driver_id = driver_id if driver_id is not None else booking.driver_id
            
            # Recalculate fare if distance changed
            if distance_km != booking.distance_km and distance_km:
                fare = calculate_fare(distance_km)
            
            # Update booking
            query = """
                UPDATE Bookings 
                SET Pickup_Location = %s, Destination = %s, Distance_KM = %s, 
                    Fare = %s, Status = %s, Driver_ID = %s
                WHERE Booking_ID = %s
            """
            rows = self.db.execute_query(
                query,
                (pickup_location, destination, distance_km, fare, status, driver_id, booking_id)
            )
            
            if rows > 0:
                return True, SUCCESS_UPDATE
            else:
                return False, "No changes made"
                
        except Exception as e:
            print(f"Update booking error: {e}")
            return False, str(e)
    
    def cancel_booking(self, booking_id):
        """
        Cancel a booking
        
        Args:
            booking_id (int): Booking ID
            
        Returns:
            tuple: (success: bool, message: str)
        """
        return self.update_booking_status(booking_id, BOOKING_STATUS_CANCELLED)
    
    def complete_booking(self, booking_id):
        """
        Mark booking as completed
        
        Args:
            booking_id (int): Booking ID
            
        Returns:
            tuple: (success: bool, message: str)
        """
        return self.update_booking_status(booking_id, BOOKING_STATUS_COMPLETED)
    
    def delete_booking(self, booking_id):
        """
        Delete booking
        
        Args:
            booking_id (int): Booking ID
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            query = "DELETE FROM Bookings WHERE Booking_ID = %s"
            rows = self.db.execute_query(query, (booking_id,))
            
            if rows > 0:
                return True, SUCCESS_DELETE
            else:
                return False, "Booking not found"
                
        except Exception as e:
            print(f"Delete booking error: {e}")
            return False, str(e)
    
    def get_total_bookings_count(self):
        """Get total number of bookings"""
        try:
            query = "SELECT COUNT(*) as count FROM Bookings"
            result = self.db.fetch_one(query)
            return result['count'] if result else 0
        except:
            return 0
    
    def get_total_revenue(self):
        """Get total revenue from completed bookings"""
        try:
            query = """
                SELECT SUM(Fare) as total 
                FROM Bookings 
                WHERE Status = %s AND Fare IS NOT NULL
            """
            result = self.db.fetch_one(query, (BOOKING_STATUS_COMPLETED,))
            return float(result['total']) if result and result['total'] else 0.0
        except:
            return 0.0
    
    def close(self):
        """Close database connection"""
        self.db.disconnect()


# Test the controller
if __name__ == "__main__":
    print("\n" + "="*60)
    print("Testing BookingController")
    print("="*60 + "\n")
    
    controller = BookingController()
    
    # Test 1: Create booking (need existing passenger_id)
    print("1. Testing booking methods...")
    print("   Note: Actual booking creation requires valid passenger_id")
    
    # Test 2: Get all bookings
    print("\n2. Getting all bookings...")
    bookings = controller.get_all_bookings()
    print(f"   Total bookings: {len(bookings)}")
    
    # Test 3: Get pending bookings
    print("\n3. Getting pending bookings...")
    pending = controller.get_pending_bookings()
    print(f"   Pending bookings: {len(pending)}")
    
    # Test 4: Get total revenue
    print("\n4. Getting total revenue...")
    revenue = controller.get_total_revenue()
    print(f"   Total revenue: ₹ {revenue:.2f}")
    
    controller.close()
    
    print("\n" + "="*60)
    print("✓ BookingController test complete")
    print("="*60 + "\n")