# Controllers/PaymentController.py
"""
Payment Controller - Handles payment management operations
"""

from Db.base_db import BaseDB
from Models.PaymentModel import PaymentModel
from config import (
    SUCCESS_REGISTRATION,
    SUCCESS_UPDATE,
    SUCCESS_DELETE,
    PAYMENT_PENDING,
    PAYMENT_COMPLETED,
    PAYMENT_FAILED,
    PAYMENT_METHODS
)
from datetime import datetime


class PaymentController:
    """
    Handles all payment-related operations
    """
    
    def __init__(self):
        """Initialize PaymentController with database connection"""
        self.db = BaseDB()
    
    def create_payment(self, booking_id, amount, payment_method, 
                      payment_status=PAYMENT_PENDING):
        """
        Create a new payment record
        
        Args:
            booking_id (int): Booking ID
            amount (float): Payment amount
            payment_method (str): Payment method
            payment_status (str): Payment status
            
        Returns:
            tuple: (success: bool, message: str, payment_id: int)
        """
        try:
            # Validate payment method
            if payment_method not in PAYMENT_METHODS:
                return False, f"Invalid payment method. Must be one of: {', '.join(PAYMENT_METHODS)}", None
            
            # Check if payment already exists for this booking
            if self.payment_exists_for_booking(booking_id):
                return False, "Payment already exists for this booking", None
            
            # Insert payment
            query = """
                INSERT INTO Payments (Booking_ID, Amount, Payment_Method, Payment_Status)
                VALUES (%s, %s, %s, %s)
            """
            rows = self.db.execute_query(
                query,
                (booking_id, amount, payment_method, payment_status)
            )
            
            if rows > 0:
                payment_id = self.db.get_last_insert_id()
                return True, SUCCESS_REGISTRATION, payment_id
            else:
                return False, "Failed to create payment", None
                
        except Exception as e:
            print(f"Create payment error: {e}")
            return False, str(e), None
    
    def get_payment_by_id(self, payment_id):
        """
        Get payment by ID
        
        Args:
            payment_id (int): Payment ID
            
        Returns:
            PaymentModel: Payment object or None
        """
        try:
            query = "SELECT * FROM Payments WHERE Payment_ID = %s"
            row = self.db.fetch_one(query, (payment_id,))
            return PaymentModel.from_db_row(row)
        except Exception as e:
            print(f"Get payment error: {e}")
            return None
    
    def get_payment_by_booking(self, booking_id):
        """
        Get payment for a specific booking
        
        Args:
            booking_id (int): Booking ID
            
        Returns:
            PaymentModel: Payment object or None
        """
        try:
            query = "SELECT * FROM Payments WHERE Booking_ID = %s"
            row = self.db.fetch_one(query, (booking_id,))
            return PaymentModel.from_db_row(row)
        except Exception as e:
            print(f"Get payment by booking error: {e}")
            return None
    
    def get_all_payments(self):
        """
        Get all payments
        
        Returns:
            list: List of PaymentModel objects
        """
        try:
            query = "SELECT * FROM Payments ORDER BY Payment_Date DESC"
            rows = self.db.fetch_all(query)
            return [PaymentModel.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Get all payments error: {e}")
            return []
    
    def get_payments_by_status(self, payment_status):
        """
        Get payments by status
        
        Args:
            payment_status (str): Payment status
            
        Returns:
            list: List of PaymentModel objects
        """
        try:
            query = """
                SELECT * FROM Payments 
                WHERE Payment_Status = %s 
                ORDER BY Payment_Date DESC
            """
            rows = self.db.fetch_all(query, (payment_status,))
            return [PaymentModel.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Get payments by status error: {e}")
            return []
    
    def get_payments_by_method(self, payment_method):
        """
        Get payments by payment method
        
        Args:
            payment_method (str): Payment method
            
        Returns:
            list: List of PaymentModel objects
        """
        try:
            query = """
                SELECT * FROM Payments 
                WHERE Payment_Method = %s 
                ORDER BY Payment_Date DESC
            """
            rows = self.db.fetch_all(query, (payment_method,))
            return [PaymentModel.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Get payments by method error: {e}")
            return []
    
    def get_pending_payments(self):
        """
        Get all pending payments
        
        Returns:
            list: List of PaymentModel objects
        """
        return self.get_payments_by_status(PAYMENT_PENDING)
    
    def get_completed_payments(self):
        """
        Get all completed payments
        
        Returns:
            list: List of PaymentModel objects
        """
        return self.get_payments_by_status(PAYMENT_COMPLETED)
    
    def get_failed_payments(self):
        """
        Get all failed payments
        
        Returns:
            list: List of PaymentModel objects
        """
        return self.get_payments_by_status(PAYMENT_FAILED)
    
    def update_payment_status(self, payment_id, payment_status):
        """
        Update payment status
        
        Args:
            payment_id (int): Payment ID
            payment_status (str): New payment status
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # If completing payment, update payment date
            if payment_status == PAYMENT_COMPLETED:
                query = """
                    UPDATE Payments 
                    SET Payment_Status = %s, Payment_Date = %s 
                    WHERE Payment_ID = %s
                """
                rows = self.db.execute_query(query, (payment_status, datetime.now(), payment_id))
            else:
                query = "UPDATE Payments SET Payment_Status = %s WHERE Payment_ID = %s"
                rows = self.db.execute_query(query, (payment_status, payment_id))
            
            if rows > 0:
                return True, SUCCESS_UPDATE
            else:
                return False, "Payment not found"
                
        except Exception as e:
            print(f"Update payment status error: {e}")
            return False, str(e)
    
    def mark_as_completed(self, payment_id):
        """
        Mark payment as completed
        
        Args:
            payment_id (int): Payment ID
            
        Returns:
            tuple: (success: bool, message: str)
        """
        return self.update_payment_status(payment_id, PAYMENT_COMPLETED)
    
    def mark_as_failed(self, payment_id):
        """
        Mark payment as failed
        
        Args:
            payment_id (int): Payment ID
            
        Returns:
            tuple: (success: bool, message: str)
        """
        return self.update_payment_status(payment_id, PAYMENT_FAILED)
    
    def update_payment(self, payment_id, amount=None, payment_method=None, 
                      payment_status=None):
        """
        Update payment information
        
        Args:
            payment_id (int): Payment ID
            amount (float): New amount (optional)
            payment_method (str): New payment method (optional)
            payment_status (str): New payment status (optional)
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Get current payment
            payment = self.get_payment_by_id(payment_id)
            if not payment:
                return False, "Payment not found"
            
            # Use current values if new ones not provided
            amount = amount if amount is not None else payment.amount
            payment_method = payment_method or payment.payment_method
            payment_status = payment_status or payment.payment_status
            
            # Validate payment method
            if payment_method not in PAYMENT_METHODS:
                return False, "Invalid payment method"
            
            # Update payment
            query = """
                UPDATE Payments 
                SET Amount = %s, Payment_Method = %s, Payment_Status = %s
                WHERE Payment_ID = %s
            """
            rows = self.db.execute_query(
                query,
                (amount, payment_method, payment_status, payment_id)
            )
            
            if rows > 0:
                return True, SUCCESS_UPDATE
            else:
                return False, "No changes made"
                
        except Exception as e:
            print(f"Update payment error: {e}")
            return False, str(e)
    
    def delete_payment(self, payment_id):
        """
        Delete payment
        
        Args:
            payment_id (int): Payment ID
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            query = "DELETE FROM Payments WHERE Payment_ID = %s"
            rows = self.db.execute_query(query, (payment_id,))
            
            if rows > 0:
                return True, SUCCESS_DELETE
            else:
                return False, "Payment not found"
                
        except Exception as e:
            print(f"Delete payment error: {e}")
            return False, str(e)
    
    def payment_exists_for_booking(self, booking_id):
        """
        Check if payment already exists for a booking
        
        Args:
            booking_id (int): Booking ID
            
        Returns:
            bool: True if payment exists
        """
        try:
            query = "SELECT Payment_ID FROM Payments WHERE Booking_ID = %s"
            result = self.db.fetch_one(query, (booking_id,))
            return result is not None
        except:
            return False
    
    def get_total_payments_count(self):
        """Get total number of payments"""
        try:
            query = "SELECT COUNT(*) as count FROM Payments"
            result = self.db.fetch_one(query)
            return result['count'] if result else 0
        except:
            return 0
    
    def get_total_revenue(self):
        """Get total revenue from completed payments"""
        try:
            query = """
                SELECT SUM(Amount) as total 
                FROM Payments 
                WHERE Payment_Status = %s
            """
            result = self.db.fetch_one(query, (PAYMENT_COMPLETED,))
            return float(result['total']) if result and result['total'] else 0.0
        except:
            return 0.0
    
    def get_revenue_by_method(self):
        """
        Get revenue breakdown by payment method
        
        Returns:
            dict: Payment method as key, revenue as value
        """
        try:
            query = """
                SELECT Payment_Method, SUM(Amount) as total
                FROM Payments
                WHERE Payment_Status = %s
                GROUP BY Payment_Method
            """
            rows = self.db.fetch_all(query, (PAYMENT_COMPLETED,))
            
            revenue_dict = {}
            for row in rows:
                method = row['Payment_Method']
                total = float(row['total']) if row['total'] else 0.0
                revenue_dict[method] = total
            
            return revenue_dict
        except:
            return {}
    
    def close(self):
        """Close database connection"""
        self.db.disconnect()

