import mysql.connector
from mysql.connector import Error

class DatabaseConnection():
    def __init__(self, host, user, password, database, port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None
        self.cursor = None

        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port
            )

            if self.connection.is_connected():
                print(f"Successfully connected to MySQL server")
                self.cursor = self.connection.cursor()
                # Create database if it doesn't exist
                self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
                print(f"Database '{self.database}' is ready")
                # Use the database
                self.cursor.execute(f"USE {self.database}")
                print(f"Using database '{self.database}'")
                
        except Error as e:
            print(f"Error connecting to database: {e}")
            self.connection = None
            self.cursor = None

    def close(self):
        """Closes the database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")
    
    def create_tables(self):
        """Create the necessary tables for the healthcare system"""
        try:
            # Create Patients table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    patient_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    age INT,
                    gender VARCHAR(10),
                    phone VARCHAR(20),
                    email VARCHAR(100),
                    address TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("Patients table created successfully")
            
            # Create Doctors table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS doctors (
                    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    specialization VARCHAR(100),
                    phone VARCHAR(20),
                    email VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("Doctors table created successfully")
            
            # Create Hospital Admins table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS admins (
                    admin_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    email VARCHAR(100),
                    phone VARCHAR(20),
                    role VARCHAR(50) DEFAULT 'admin',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("Admins table created successfully")
            
            self.connection.commit()
            print("All tables created successfully!")
            
        except Error as e:
            print(f"Error creating tables: {e}")


# Create AUTH database connection
auth_db = DatabaseConnection(
    host="mysql-ea2e4c1-alustudent-32a5.f.aivencloud.com",
    user="avnadmin",
    password="AVNS_tvNAcoOEUSfzYG3i7NC",
    database="Healthcare_Auth_DB",
    port=27806
)

# Create tables in auth database
auth_db.create_tables()


# Create APPLICATION database connection - for appointments, records, etc.
app_db = DatabaseConnection(
    host="mysql-ea2e4c1-alustudent-32a5.f.aivencloud.com",
    user="avnadmin",
    password="AVNS_tvNAcoOEUSfzYG3i7NC",
    database="Heathcare_Data_System",  # Separate database for application data
    port=27806
)
