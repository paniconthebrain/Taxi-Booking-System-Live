import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        # UPDATE THESE VALUES TO MATCH YOUR MYSQL SERVER
        self.host = "localhost"
        self.user = "root"
        self.password = "1234"
        self.database = "taxi_booking_system"

        self.create_database()
        self.connection = self.connect()

    def connect(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return conn
        except Error as e:
            print("Error connecting to MySQL:", e)
            return None

    def create_database(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS taxi_booking_system")
            conn.close()
        except Error as e:
            print("Error creating database:", e)

    def table_create(self):
        conn = self.connect()
        cursor = conn.cursor()

        # USERS TABLE
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Login(
                Login_Id INT AUTO_INCREMENT PRIMARY KEY,
                User_Name VARCHAR(255) UNIQUE NOT NULL,
                Email VARCHAR(255) UNIQUE NOT NULL,
                Password VARCHAR(255) NOT NULL,
                UserType VARCHAR(50) DEFAULT 'customer'
            )
        """)

        # DRIVERS TABLE
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Driver_Info(
                Driver_Id INT AUTO_INCREMENT PRIMARY KEY,
                Full_Name VARCHAR(255) NOT NULL,
                Contact_No VARCHAR(20) UNIQUE NOT NULL,
                License_Id_No VARCHAR(50) UNIQUE NOT NULL,
                Current_Status VARCHAR(50) DEFAULT 'Active'
            )
        """)

        # VEHICLES TABLE
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Driver_Vehicle(
                Vehicle_Id INT AUTO_INCREMENT PRIMARY KEY,
                Driver_Id INT,
                Vehicle_No VARCHAR(50) UNIQUE NOT NULL,
                Vehicle_Type VARCHAR(50) DEFAULT 'Taxi',
                Vehicle_Image TEXT,
                FOREIGN KEY (Driver_Id) REFERENCES Driver_Info(Driver_Id)
                    ON DELETE SET NULL
            )
        """)

        # BOOKING TABLE
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Booking_History(
                Booking_Id INT AUTO_INCREMENT PRIMARY KEY,
                Login_Id INT,
                Driver_Id INT,
                -- Assigned_Vehicle_Id INT,
                Pickup_Location VARCHAR(255),
                Pickup_Time VARCHAR(255),
                Drop_Location VARCHAR(255),
                Fare FLOAT,
                Booking_Status VARCHAR(50) DEFAULT 'On-Going',
                FOREIGN KEY (Login_Id) REFERENCES Login(Login_Id),
                FOREIGN KEY (Driver_Id) REFERENCES Driver_Info(Driver_Id),
                FOREIGN KEY (Assigned_Vehicle_Id) REFERENCES Driver_Vehicle(Vehicle_Id)
            )
        """)

        conn.commit()
        conn.close()
        print("MySQL Tables created successfully ✔")
