# config.py
"""
Global Configuration File
Contains all application-wide settings for UI, colors, fonts, and database
"""

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '1234',
    'database': 'taxi_booking_db'
}

# Default Admin Credentials
DEFAULT_ADMIN = {
    'username': 'admin',
    'password': 'admin123',
    'user_type': 'Admin'
}


# =============================================================================
# APPLICATION WINDOW SETTINGS
# =============================================================================

# Main Window
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1200
WINDOW_TITLE = "Taxi Booking System test"

# Login Window
LOGIN_WINDOW_WIDTH = 450
LOGIN_WINDOW_HEIGHT = 700

# Dashboard Window
DASHBOARD_WIDTH = 1400
DASHBOARD_HEIGHT = 800


# =============================================================================
# COLOR SCHEME
# =============================================================================

# Primary Colors
PRIMARY_COLOR = "#2C3E50"       # Dark Blue-Gray
SECONDARY_COLOR = "#3498DB"     # Bright Blue
ACCENT_COLOR = "#E74C3C"        # Red
SUCCESS_COLOR = "#27AE60"       # Green
WARNING_COLOR = "#F39C12"       # Orange
INFO_COLOR = "#3498DB"          # Blue

# Background Colors
BG_COLOR = "#ECF0F1"            # Light Gray
BG_DARK = "#2C3E50"             # Dark Background
BG_LIGHT = "#FFFFFF"            # White
SIDEBAR_BG = "#34495E"          # Dark Gray

# Text Colors
TEXT_PRIMARY = "#2C3E50"        # Dark Text
TEXT_SECONDARY = "#7F8C8D"      # Gray Text
TEXT_LIGHT = "#FFFFFF"          # White Text
TEXT_DARK = "#000000"           # Black Text

# Button Colors
BTN_PRIMARY = "#3498DB"         # Blue Button
BTN_PRIMARY_HOVER = "#2980B9"   # Darker Blue
BTN_SUCCESS = "#27AE60"         # Green Button
BTN_SUCCESS_HOVER = "#229954"   # Darker Green
BTN_DANGER = "#E74C3C"          # Red Button
BTN_DANGER_HOVER = "#C0392B"    # Darker Red
BTN_WARNING = "#F39C12"         # Orange Button
BTN_SECONDARY = "#95A5A6"       # Gray Button

# Input Field Colors
INPUT_BG = "#FFFFFF"
INPUT_BORDER = "#BDC3C7"
INPUT_FOCUS_BORDER = "#3498DB"
INPUT_ERROR_BORDER = "#E74C3C"

# Table/List Colors
TABLE_HEADER_BG = "#34495E"
TABLE_HEADER_FG = "#FFFFFF"
TABLE_ROW_BG = "#FFFFFF"
TABLE_ALT_ROW_BG = "#ECF0F1"
TABLE_SELECT_BG = "#3498DB"
TABLE_SELECT_FG = "#FFFFFF"


# =============================================================================
# FONTS
# =============================================================================

# Font Families
FONT_FAMILY = "Segoe UI"
FONT_FAMILY_MONO = "Consolas"
FONT_FAMILY_ALT = "Arial"

# Font Sizes
FONT_SIZE_SMALL = 9
FONT_SIZE_NORMAL = 10
FONT_SIZE_MEDIUM = 11
FONT_SIZE_LARGE = 12
FONT_SIZE_XLARGE = 14
FONT_SIZE_TITLE = 16
FONT_SIZE_HEADING = 18
FONT_SIZE_LARGE_HEADING = 24

# Font Weights
FONT_NORMAL = "normal"
FONT_BOLD = "bold"

# Complete Font Configurations
FONT_SMALL = (FONT_FAMILY, FONT_SIZE_SMALL, FONT_NORMAL)
FONT_NORMAL_REGULAR = (FONT_FAMILY, FONT_SIZE_NORMAL, FONT_NORMAL)
FONT_NORMAL_BOLD = (FONT_FAMILY, FONT_SIZE_NORMAL, FONT_BOLD)
FONT_MEDIUM = (FONT_FAMILY, FONT_SIZE_MEDIUM, FONT_NORMAL)
FONT_MEDIUM_BOLD = (FONT_FAMILY, FONT_SIZE_MEDIUM, FONT_BOLD)
FONT_LARGE = (FONT_FAMILY, FONT_SIZE_LARGE, FONT_NORMAL)
FONT_LARGE_BOLD = (FONT_FAMILY, FONT_SIZE_LARGE, FONT_BOLD)
FONT_TITLE = (FONT_FAMILY, FONT_SIZE_TITLE, FONT_BOLD)
FONT_HEADING = (FONT_FAMILY, FONT_SIZE_HEADING, FONT_BOLD)
FONT_LARGE_HEADING = (FONT_FAMILY, FONT_SIZE_LARGE_HEADING, FONT_BOLD)


# =============================================================================
# SPACING & PADDING
# =============================================================================

# Padding
PADDING_SMALL = 5
PADDING_MEDIUM = 10
PADDING_LARGE = 15
PADDING_XLARGE = 20

# Margins
MARGIN_SMALL = 5
MARGIN_MEDIUM = 10
MARGIN_LARGE = 15
MARGIN_XLARGE = 20

# Border Radius
BORDER_RADIUS_SMALL = 3
BORDER_RADIUS_MEDIUM = 5
BORDER_RADIUS_LARGE = 8

# Border Width
BORDER_WIDTH_THIN = 1
BORDER_WIDTH_MEDIUM = 2
BORDER_WIDTH_THICK = 3


# =============================================================================
# WIDGET DIMENSIONS
# =============================================================================

# Entry/Input Fields
ENTRY_WIDTH_SMALL = 15
ENTRY_WIDTH_MEDIUM = 25
ENTRY_WIDTH_LARGE = 35
ENTRY_HEIGHT = 30

# Buttons
BUTTON_WIDTH_SMALL = 8
BUTTON_WIDTH_MEDIUM = 12
BUTTON_WIDTH_LARGE = 18
BUTTON_HEIGHT = 35

# Listbox/Table
LISTBOX_WIDTH = 40
LISTBOX_HEIGHT = 15


# =============================================================================
# USER ROLES
# =============================================================================

USER_TYPE_ADMIN = "Admin"
USER_TYPE_PASSENGER = "Passenger"
USER_TYPE_DRIVER = "Driver"

USER_TYPES = [USER_TYPE_ADMIN, USER_TYPE_PASSENGER, USER_TYPE_DRIVER]


# =============================================================================
# BOOKING STATUS
# =============================================================================

BOOKING_STATUS_PENDING = "Pending"
BOOKING_STATUS_CONFIRMED = "Confirmed"
BOOKING_STATUS_IN_PROGRESS = "In Progress"
BOOKING_STATUS_COMPLETED = "Completed"
BOOKING_STATUS_CANCELLED = "Cancelled"

BOOKING_STATUSES = [
    BOOKING_STATUS_PENDING,
    BOOKING_STATUS_CONFIRMED,
    BOOKING_STATUS_IN_PROGRESS,
    BOOKING_STATUS_COMPLETED,
    BOOKING_STATUS_CANCELLED
]


# =============================================================================
# DRIVER AVAILABILITY
# =============================================================================

DRIVER_AVAILABLE = "Available"
DRIVER_BUSY = "Busy"
DRIVER_OFFLINE = "Offline"

DRIVER_STATUSES = [DRIVER_AVAILABLE, DRIVER_BUSY, DRIVER_OFFLINE]


# =============================================================================
# VEHICLE TYPES
# =============================================================================

VEHICLE_SEDAN = "Sedan"
VEHICLE_SUV = "SUV"
VEHICLE_HATCHBACK = "Hatchback"
VEHICLE_LUXURY = "Luxury"

VEHICLE_TYPES = [VEHICLE_SEDAN, VEHICLE_SUV, VEHICLE_HATCHBACK, VEHICLE_LUXURY]


# =============================================================================
# PAYMENT METHODS
# =============================================================================

PAYMENT_CASH = "Cash"
PAYMENT_CARD = "Card"
PAYMENT_UPI = "UPI"
PAYMENT_WALLET = "Wallet"

PAYMENT_METHODS = [PAYMENT_CASH, PAYMENT_CARD, PAYMENT_UPI, PAYMENT_WALLET]


# =============================================================================
# PAYMENT STATUS
# =============================================================================

PAYMENT_PENDING = "Pending"
PAYMENT_COMPLETED = "Completed"
PAYMENT_FAILED = "Failed"

PAYMENT_STATUSES = [PAYMENT_PENDING, PAYMENT_COMPLETED, PAYMENT_FAILED]


# =============================================================================
# VALIDATION PATTERNS
# =============================================================================

import re

# Regex Patterns
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
PHONE_PATTERN = re.compile(r'^[0-9]{10}$')
LICENSE_PATTERN = re.compile(r'^[A-Z0-9]{8,15}$')
LICENSE_PLATE_PATTERN = re.compile(r'^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$')

# Validation Functions
def validate_email(email):
    """Validate email format"""
    return bool(EMAIL_PATTERN.match(email))

def validate_phone(phone):
    """Validate phone number (10 digits)"""
    return bool(PHONE_PATTERN.match(phone))

def validate_license(license_number):
    """Validate driver license number"""
    return bool(LICENSE_PATTERN.match(license_number.upper()))

def validate_license_plate(plate):
    """Validate vehicle license plate"""
    return bool(LICENSE_PLATE_PATTERN.match(plate.upper()))


# =============================================================================
# APPLICATION SETTINGS
# =============================================================================

# Debug Mode
DEBUG_MODE = False

# Date Format
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT_SHORT = "%Y-%m-%d"
DATE_FORMAT_DISPLAY = "%d-%m-%Y %I:%M %p"

# Currency
CURRENCY_SYMBOL = "₹"
CURRENCY_FORMAT = "{} {:.2f}"

# Distance Unit
DISTANCE_UNIT = "km"

# Fare Calculation (per km)
BASE_FARE = 50.0
FARE_PER_KM = 15.0

def calculate_fare(distance_km):
    """Calculate fare based on distance"""
    return BASE_FARE + (distance_km * FARE_PER_KM)


# =============================================================================
# ERROR MESSAGES
# =============================================================================

ERROR_DB_CONNECTION = "Failed to connect to database. Please check your connection settings."
ERROR_INVALID_CREDENTIALS = "Invalid username or password."
ERROR_USER_EXISTS = "Username already exists."
ERROR_EMAIL_EXISTS = "Email already exists."
ERROR_PHONE_EXISTS = "Phone number already exists."
ERROR_LICENSE_EXISTS = "License number already exists."
ERROR_REQUIRED_FIELD = "This field is required."
ERROR_INVALID_EMAIL = "Invalid email format."
ERROR_INVALID_PHONE = "Invalid phone number. Must be 10 digits."
ERROR_INVALID_LICENSE = "Invalid license number format."
ERROR_INVALID_PLATE = "Invalid license plate format."
ERROR_PASSWORD_MISMATCH = "Passwords do not match."
ERROR_WEAK_PASSWORD = "Password must be at least 6 characters."


# =============================================================================
# SUCCESS MESSAGES
# =============================================================================

SUCCESS_LOGIN = "Login successful!"
SUCCESS_REGISTRATION = "Registration successful!"
SUCCESS_BOOKING = "Booking created successfully!"
SUCCESS_UPDATE = "Updated successfully!"
SUCCESS_DELETE = "Deleted successfully!"
SUCCESS_PAYMENT = "Payment completed successfully!"


# =============================================================================
# INFO MESSAGES
# =============================================================================

INFO_NO_DRIVERS = "No drivers available at the moment."
INFO_NO_BOOKINGS = "No bookings found."
INFO_NO_DATA = "No data available."