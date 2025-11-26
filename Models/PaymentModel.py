# Models/PaymentModel.py
"""
Payment Model - Represents Payments table
"""

from datetime import datetime
from config import (
    PAYMENT_CASH,
    PAYMENT_PENDING,
    PAYMENT_COMPLETED,
    PAYMENT_FAILED,
    CURRENCY_SYMBOL
)


class PaymentModel:
    """
    Represents a payment transaction in the system
    """
    
    def __init__(self, payment_id=None, booking_id=None, amount=None,
                 payment_method=None, payment_status=None, payment_date=None):
        """
        Initialize Payment Model
        
        Args:
            payment_id (int): Unique payment identifier
            booking_id (int): Reference to booking
            amount (float): Payment amount
            payment_method (str): Method of payment
            payment_status (str): Current payment status
            payment_date (datetime): Payment timestamp
        """
        self.payment_id = payment_id
        self.booking_id = booking_id
        self.amount = amount
        self.payment_method = payment_method or PAYMENT_CASH
        self.payment_status = payment_status or PAYMENT_PENDING
        self.payment_date = payment_date or datetime.now()
    
    @staticmethod
    def from_db_row(row):
        """
        Create PaymentModel instance from database row
        
        Args:
            row (dict): Database row as dictionary
            
        Returns:
            PaymentModel: Payment model instance
        """
        if not row:
            return None
        
        return PaymentModel(
            payment_id=row.get('Payment_ID'),
            booking_id=row.get('Booking_ID'),
            amount=float(row.get('Amount')) if row.get('Amount') else None,
            payment_method=row.get('Payment_Method'),
            payment_status=row.get('Payment_Status'),
            payment_date=row.get('Payment_Date')
        )
    
    def to_dict(self):
        """
        Convert model to dictionary
        
        Returns:
            dict: Payment data as dictionary
        """
        return {
            'payment_id': self.payment_id,
            'booking_id': self.booking_id,
            'amount': self.amount,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'payment_date': self.payment_date
        }
    
    def is_pending(self):
        """Check if payment is pending"""
        return self.payment_status == PAYMENT_PENDING
    
    def is_completed(self):
        """Check if payment is completed"""
        return self.payment_status == PAYMENT_COMPLETED
    
    def is_failed(self):
        """Check if payment failed"""
        return self.payment_status == PAYMENT_FAILED
    
    def mark_completed(self):
        """Mark payment as completed"""
        self.payment_status = PAYMENT_COMPLETED
        self.payment_date = datetime.now()
    
    def mark_failed(self):
        """Mark payment as failed"""
        self.payment_status = PAYMENT_FAILED
    
    def get_formatted_amount(self):
        """Get formatted amount with currency symbol"""
        return f"{CURRENCY_SYMBOL} {self.amount:.2f}"
    
    def __str__(self):
        """String representation"""
        return f"Payment(ID={self.payment_id}, Amount={self.get_formatted_amount()}, Status={self.payment_status})"
    
    def __repr__(self):
        """Developer representation"""
        return self.__str__()