# Db/DatabaseCRUD.py
"""
Database Setup & Table Creation
Creates all necessary tables and inserts default admin user
"""

from Db.base_db import BaseDB
from config import (
    DEFAULT_ADMIN,
    USER_TYPES,
    BOOKING_STATUSES,
    DRIVER_STATUSES,
    VEHICLE_TYPES,
    PAYMENT_METHODS,
    PAYMENT_STATUSES,
    DRIVER_AVAILABLE
)
import hashlib


class DatabaseCRUD(BaseDB):
    """
    Handles database schema creation and initial setup
    """
    
    def __init__(self):
        super().__init__()
    
    def create_all_tables(self):
        """Create all tables required for the taxi booking system"""
        print("\n" + "="*50)
        print("Creating Database Tables...")
        print("="*50)
        
        try:
            self.create_login_table()
            self.create_passengers_table()
            self.create_drivers_table()
            self.create_vehicles_table()
            self.create_bookings_table()
            self.create_payments_table()
            
            print("="*50)
            print("✓ All tables created successfully!")
            print("="*50 + "\n")
            return True
            
        except Exception as e:
            print("="*50)
            print(f"✗ Error creating tables: {e}")
            print("="*50 + "\n")
            return False
    
    def create_login_table(self):
        """Create Login table for user authentication"""
        user_types_enum = "', '".join(USER_TYPES)
        query = f"""
        CREATE TABLE IF NOT EXISTS Login (
            User_ID INT AUTO_INCREMENT PRIMARY KEY,
            Username VARCHAR(50) UNIQUE NOT NULL,
            Password VARCHAR(255) NOT NULL,
            User_Type ENUM('{user_types_enum}') NOT NULL,
            Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_username (Username),
            INDEX idx_user_type (User_Type)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        self.execute_query(query)
        print("✓ Login table created")
    
    def create_passengers_table(self):
        """Create Passengers table"""
        query = """
        CREATE TABLE IF NOT EXISTS Passengers (
            Passenger_ID INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(100) NOT NULL,
            Email VARCHAR(100) UNIQUE NOT NULL,
            Phone VARCHAR(15) NOT NULL,
            Address TEXT,
            User_ID INT UNIQUE,
            Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (User_ID) REFERENCES Login(User_ID) ON DELETE CASCADE,
            INDEX idx_email (Email),
            INDEX idx_phone (Phone),
            INDEX idx_user_id (User_ID)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        self.execute_query(query)
        print("✓ Passengers table created")
    
    def create_drivers_table(self):
        """Create Drivers table"""
        driver_statuses_enum = "', '".join(DRIVER_STATUSES)
        query = f"""
        CREATE TABLE IF NOT EXISTS Drivers (
            Driver_ID INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(100) NOT NULL,
            License_Number VARCHAR(50) UNIQUE NOT NULL,
            Phone VARCHAR(15) NOT NULL,
            Email VARCHAR(100),
            Availability ENUM('{driver_statuses_enum}') DEFAULT '{DRIVER_AVAILABLE}',
            User_ID INT UNIQUE,
            Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (User_ID) REFERENCES Login(User_ID) ON DELETE CASCADE,
            INDEX idx_license (License_Number),
            INDEX idx_availability (Availability),
            INDEX idx_user_id (User_ID)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        self.execute_query(query)
        print("✓ Drivers table created")
    
    def create_vehicles_table(self):
        """Create Vehicles table"""
        vehicle_types_enum = "', '".join(VEHICLE_TYPES)
        query = f"""
        CREATE TABLE IF NOT EXISTS Vehicles (
            Vehicle_ID INT AUTO_INCREMENT PRIMARY KEY,
            Model VARCHAR(100) NOT NULL,
            License_Plate VARCHAR(20) UNIQUE NOT NULL,
            Vehicle_Type ENUM('{vehicle_types_enum}') DEFAULT '{VEHICLE_TYPES[0]}',
            Color VARCHAR(30),
            Year INT,
            Driver_ID INT UNIQUE,
            Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (Driver_ID) REFERENCES Drivers(Driver_ID) ON DELETE SET NULL,
            INDEX idx_license_plate (License_Plate),
            INDEX idx_driver_id (Driver_ID)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        self.execute_query(query)
        print("✓ Vehicles table created")
    
    def create_bookings_table(self):
        """Create Bookings table"""
        booking_statuses_enum = "', '".join(BOOKING_STATUSES)
        query = f"""
        CREATE TABLE IF NOT EXISTS Bookings (
            Booking_ID INT AUTO_INCREMENT PRIMARY KEY,
            Passenger_ID INT NOT NULL,
            Driver_ID INT,
            Pickup_Location VARCHAR(255) NOT NULL,
            Destination VARCHAR(255) NOT NULL,
            Status ENUM('{booking_statuses_enum}') DEFAULT '{BOOKING_STATUSES[0]}',
            Fare DECIMAL(10, 2),
            Distance_KM DECIMAL(10, 2),
            Booking_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            Completion_Date TIMESTAMP NULL,
            FOREIGN KEY (Passenger_ID) REFERENCES Passengers(Passenger_ID) ON DELETE CASCADE,
            FOREIGN KEY (Driver_ID) REFERENCES Drivers(Driver_ID) ON DELETE SET NULL,
            INDEX idx_passenger (Passenger_ID),
            INDEX idx_driver (Driver_ID),
            INDEX idx_status (Status),
            INDEX idx_booking_date (Booking_Date)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        self.execute_query(query)
        print("✓ Bookings table created")
    
    def create_payments_table(self):
        """Create Payments table"""
        payment_methods_enum = "', '".join(PAYMENT_METHODS)
        payment_statuses_enum = "', '".join(PAYMENT_STATUSES)
        query = f"""
        CREATE TABLE IF NOT EXISTS Payments (
            Payment_ID INT AUTO_INCREMENT PRIMARY KEY,
            Booking_ID INT UNIQUE NOT NULL,
            Amount DECIMAL(10, 2) NOT NULL,
            Payment_Method ENUM('{payment_methods_enum}') DEFAULT '{PAYMENT_METHODS[0]}',
            Payment_Status ENUM('{payment_statuses_enum}') DEFAULT '{PAYMENT_STATUSES[0]}',
            Payment_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (Booking_ID) REFERENCES Bookings(Booking_ID) ON DELETE CASCADE,
            INDEX idx_payment_status (Payment_Status),
            INDEX idx_payment_date (Payment_Date),
            INDEX idx_booking_id (Booking_ID)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        self.execute_query(query)
        print("✓ Payments table created")
    
    def hash_password(self, password):
        """
        Hash password using SHA-256
        
        Args:
            password (str): Plain text password
            
        Returns:
            str: Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def insert_default_admin(self):
        """Insert default admin user if not exists"""
        try:
            # Check if admin already exists
            check_query = "SELECT User_ID FROM Login WHERE Username = %s"
            existing_admin = self.fetch_one(check_query, (DEFAULT_ADMIN['username'],))
            
            if existing_admin:
                print(f"ℹ  Default admin already exists (User_ID: {existing_admin['User_ID']})")
                return True
            
            # Insert default admin
            hashed_password = self.hash_password(DEFAULT_ADMIN['password'])
            insert_query = """
                INSERT INTO Login (Username, Password, User_Type)
                VALUES (%s, %s, %s)
            """
            rows = self.execute_query(
                insert_query,
                (DEFAULT_ADMIN['username'], hashed_password, DEFAULT_ADMIN['user_type'])
            )
            
            if rows > 0:
                print(f"✓ Default admin created")
                print(f"  Username: {DEFAULT_ADMIN['username']}")
                print(f"  Password: {DEFAULT_ADMIN['password']}")
                return True
            else:
                print("✗ Failed to create default admin")
                return False
                
        except Exception as e:
            print(f"✗ Error creating default admin: {e}")
            return False
    
    def setup_database(self):
        """Complete database setup - creates tables and default admin"""
        print("\n" + "🚕 "*20)
        print("TAXI BOOKING SYSTEM - DATABASE SETUP")
        print("🚕 "*20 + "\n")
        
        success = True
        
        # Create tables
        if not self.create_all_tables():
            success = False
        
        # Insert default admin
        if not self.insert_default_admin():
            success = False
        
        if success:
            print("\n" + "="*50)
            print("✓ Database setup completed successfully!")
            print("="*50)
            print("\nYou can now run the application.")
            print(f"Default admin credentials:")
            print(f"  Username: {DEFAULT_ADMIN['username']}")
            print(f"  Password: {DEFAULT_ADMIN['password']}")
            print("="*50 + "\n")
        else:
            print("\n" + "="*50)
            print("⚠  Database setup completed with warnings")
            print("="*50 + "\n")
        
        return success
    
    def reset_database(self):
        """Drop all tables (use with caution!)"""
        tables = ['Payments', 'Bookings', 'Vehicles', 'Drivers', 'Passengers', 'Login']
        
        print("\n" + "="*50)
        print("⚠  WARNING: DROPPING ALL TABLES")
        print("="*50)
        
        for table in tables:
            try:
                query = f"DROP TABLE IF EXISTS {table}"
                self.execute_query(query)
                print(f"✓ Dropped table: {table}")
            except Exception as e:
                print(f"✗ Error dropping table {table}: {e}")
        
        print("="*50)
        print("✓ Database reset complete")
        print("="*50 + "\n")
    
    def get_database_info(self):
        """Get information about the current database"""
        print("\n" + "="*50)
        print("DATABASE INFORMATION")
        print("="*50)
        
        tables = ['Login', 'Passengers', 'Drivers', 'Vehicles', 'Bookings', 'Payments']
        
        for table in tables:
            if self.table_exists(table):
                count = self.get_table_row_count(table)
                print(f"✓ {table}: {count} records")
            else:
                print(f"✗ {table}: Table does not exist")
        
        print("="*50 + "\n")


# Test and setup
if __name__ == "__main__":
    try:
        db_setup = DatabaseCRUD()
        
        # Uncomment the following line to reset database (CAUTION!)
        # db_setup.reset_database()
        
        # Setup database
        db_setup.setup_database()
        
        # Show database info
        db_setup.get_database_info()
        
        db_setup.disconnect()
        
    except Exception as e:
        print(f"\n✗ Setup failed: {e}\n")