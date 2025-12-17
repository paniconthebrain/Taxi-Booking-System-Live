from datetime import datetime
from config import (BOOKING_STATUS_PENDING,BOOKING_STATUS_CONFIRMED,BOOKING_STATUS_IN_PROGRESS,BOOKING_STATUS_COMPLETED,BOOKING_STATUS_CANCELLED,calculate_fare,CURRENCY_SYMBOL
)

class BookingModel:

    def __init__(self, booking_id=None, passenger_id=None, driver_id=None,
                 pickup_location=None, destination=None, status=None,
                 fare=None, distance_km=None, booking_date=None, 
                 completion_date=None):

        self.booking_id = booking_id
        self.passenger_id = passenger_id
        self.driver_id = driver_id
        self.pickup_location = pickup_location
        self.destination = destination
        self.status = status or BOOKING_STATUS_PENDING
        self.fare = fare
        self.distance_km = distance_km
        self.booking_date = booking_date or datetime.now()
        self.completion_date = completion_date
    
    @staticmethod
    def from_db_row(row):
        """
        Create BookingModel instance from database row
        
        Args:
            row (dict): Database row as dictionary
            
        Returns:
            BookingModel: Booking model instance
        """
        if not row:
            return None
        
        return BookingModel(
            booking_id=row.get('Booking_ID'),
            passenger_id=row.get('Passenger_ID'),
            driver_id=row.get('Driver_ID'),
            pickup_location=row.get('Pickup_Location'),
            destination=row.get('Destination'),
            status=row.get('Status'),
            fare=float(row.get('Fare')) if row.get('Fare') else None,
            distance_km=float(row.get('Distance_KM')) if row.get('Distance_KM') else None,
            booking_date=row.get('Booking_Date'),
            completion_date=row.get('Completion_Date')
        )
    
    def to_dict(self):
        """
        Convert model to dictionary
        
        Returns:
            dict: Booking data as dictionary
        """
        return {
            'booking_id': self.booking_id,
            'passenger_id': self.passenger_id,
            'driver_id': self.driver_id,
            'pickup_location': self.pickup_location,
            'destination': self.destination,
            'status': self.status,
            'fare': self.fare,
            'distance_km': self.distance_km,
            'booking_date': self.booking_date,
            'completion_date': self.completion_date
        }
    
    def calculate_and_set_fare(self, distance_km):
        """
        Calculate and set fare based on distance
        
        Args:
            distance_km (float): Distance in kilometers
        """
        self.distance_km = distance_km
        self.fare = calculate_fare(distance_km)
    
    def is_pending(self):
        """Check if booking is pending"""
        return self.status == BOOKING_STATUS_PENDING
    
    def is_confirmed(self):
        """Check if booking is confirmed"""
        return self.status == BOOKING_STATUS_CONFIRMED
    
    def is_in_progress(self):
        """Check if booking is in progress"""
        return self.status == BOOKING_STATUS_IN_PROGRESS
    
    def is_completed(self):
        """Check if booking is completed"""
        return self.status == BOOKING_STATUS_COMPLETED
    
    def is_cancelled(self):
        """Check if booking is cancelled"""
        return self.status == BOOKING_STATUS_CANCELLED
    
    def has_driver(self):
        """Check if driver is assigned"""
        return self.driver_id is not None
    
    def set_pending(self):
        """Set status to pending"""
        self.status = BOOKING_STATUS_PENDING
    
    def set_confirmed(self):
        """Set status to confirmed"""
        self.status = BOOKING_STATUS_CONFIRMED
    
    def set_in_progress(self):
        """Set status to in progress"""
        self.status = BOOKING_STATUS_IN_PROGRESS
    
    def set_completed(self):
        """Set status to completed"""
        self.status = BOOKING_STATUS_COMPLETED
        self.completion_date = datetime.now()
    
    def set_cancelled(self):
        """Set status to cancelled"""
        self.status = BOOKING_STATUS_CANCELLED
    
    def get_route_display(self):
        """Get formatted route display"""
        return f"{self.pickup_location} → {self.destination}"
    
    def get_formatted_fare(self):
        """Get formatted fare with currency"""
        if self.fare:
            return f"{CURRENCY_SYMBOL} {self.fare:.2f}"
        return "N/A"
    
    def get_formatted_distance(self):
        """Get formatted distance"""
        if self.distance_km:
            return f"{self.distance_km:.2f} km"
        return "N/A"
    
    def get_status_color(self):
        """Get color code for booking status"""
        colors = {
            BOOKING_STATUS_PENDING: "#F39C12",      # Orange
            BOOKING_STATUS_CONFIRMED: "#3498DB",    # Blue
            BOOKING_STATUS_IN_PROGRESS: "#9B59B6",  # Purple
            BOOKING_STATUS_COMPLETED: "#27AE60",    # Green
            BOOKING_STATUS_CANCELLED: "#E74C3C"     # Red
        }
        return colors.get(self.status, "#95A5A6")
    
    def __str__(self):
        """String representation"""
        return f"Booking(ID={self.booking_id}, Route={self.get_route_display()}, Status={self.status})"
    
    def __repr__(self):
        """Developer representation"""
        return self.__str__()