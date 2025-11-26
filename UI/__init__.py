# UI/__init__.py
"""
UI Package
Contains all user interface components for the Taxi Booking System
"""

from UI.LoginPage import LoginPage
from UI.RegistrationPage import RegistrationPage
from UI.Dashboard_Admin import AdminDashboard
from UI.Dashboard_Passenger import PassengerDashboard
from UI.Dashboard_Driver import DriverDashboard

__all__ = [
    'LoginPage',
    'RegistrationPage',
    'AdminDashboard',
    'PassengerDashboard',
    'DriverDashboard'
]