import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class DatabaseConnection():
    def __init__(self):
        # Get database credentials from environment variables
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")
        self.port = int(os.getenv("DB_PORT", 3306))  # default MySQL port 3306
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establish a database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print("Database connection established")
        except Error as e:
            print(f"Error connecting to database: {e}")
            self.connection = None
            self.cursor = None

    def close(self):
        """Close the database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

    def create_tables(self):
        """Create tables in the database"""
        try:
            self.cursor.execute("""
              CREATE TABLE IF NOT EXISTS patients (
                    patient_id INT AUTO_INCREMENT PRIMARY KEY,
                    patient_name VARCHAR(100) NOT NULL,
                    patient_age INT,
                    patient_gender VARCHAR(10),
                    patient_phone VARCHAR(20),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                  )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS doctors (
                    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
                    doctor_name VARCHAR(100) NOT NULL,
                    doctor_specialization VARCHAR(100),
                    doctor_phone VARCHAR(20),
                    doctor_email VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS admins (
                    admin_id INT AUTO_INCREMENT PRIMARY KEY,
                    admin_name VARCHAR(100) NOT NULL,
                    admin_email VARCHAR(100),
                    admin_phone VARCHAR(20),
                    role VARCHAR(50) DEFAULT 'admin',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("Tables created successfully")
        except Error as e:
            print(f"Error creating tables: {e}") 


# Usage example:
db = DatabaseConnection()
db.connect()
db.create_tables()
db.close()
