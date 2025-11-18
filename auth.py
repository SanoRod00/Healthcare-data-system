import hashlib
from database import auth_db

class Auth:
    """Authentication system for patients, doctors, and admins"""
    
    def __init__(self):
        """Initialize the Auth class"""
        self.db = auth_db  
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_patient(self, username, password, name, age, gender, phone, email, address):
        """Register a new patient"""
        try:
            hashed_password = self.hash_password(password)
            query = """
                INSERT INTO patients (username, password, name, age, gender, phone, email, address)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.db.cursor.execute(query, (username, hashed_password, name, age, gender, phone, email, address))
            self.db.connection.commit()
            print(f"Patient '{username}' registered successfully!")
            return True
        except Exception as e:
            print(f"Error registering patient: {e}")
            return False
    
    def register_doctor(self, username, password, name, specialization, phone, email):
        """Register a new doctor"""
        try:
            hashed_password = self.hash_password(password)
            query = """
                INSERT INTO doctors (username, password, name, specialization, phone, email)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.db.cursor.execute(query, (username, hashed_password, name, specialization, phone, email))
            self.db.connection.commit()
            print(f"Doctor '{username}' registered successfully!")
            return True
        except Exception as e:
            print(f"Error registering doctor: {e}")
            return False
    
    def register_admin(self, username, password, name, email, phone, role="admin"):
        """Register a new admin"""
        try:
            hashed_password = self.hash_password(password)
            query = """
                INSERT INTO admins (username, password, name, email, phone, role)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.db.cursor.execute(query, (username, hashed_password, name, email, phone, role))
            self.db.connection.commit()
            print(f"Admin '{username}' registered successfully!")
            return True
        except Exception as e:
            print(f"Error registering admin: {e}")
            return False
    
    def login_patient(self, username, password):
        """Authenticate a patient"""
        try:
            hashed_password = self.hash_password(password)
            query = "SELECT * FROM patients WHERE username = %s AND password = %s"
            self.db.cursor.execute(query, (username, hashed_password))
            result = self.db.cursor.fetchone()
            
            if result:
                print(f"Patient '{username}' logged in successfully!")
                return {
                    "patient_id": result[0],
                    "username": result[1],
                    "name": result[3],
                    "age": result[4],
                    "gender": result[5],
                    "phone": result[6],
                    "email": result[7],
                    "address": result[8]
                }
            else:
                print("Invalid username or password!")
                return None
        except Exception as e:
            print(f"Error logging in: {e}")
            return None
    
    def login_doctor(self, username, password):
        """Authenticate a doctor"""
        try:
            hashed_password = self.hash_password(password)
            query = "SELECT * FROM doctors WHERE username = %s AND password = %s"
            self.db.cursor.execute(query, (username, hashed_password))
            result = self.db.cursor.fetchone()
            
            if result:
                print(f"Doctor '{username}' logged in successfully!")
                return {
                    "doctor_id": result[0],
                    "username": result[1],
                    "name": result[3],
                    "specialization": result[4],
                    "phone": result[5],
                    "email": result[6]
                }
            else:
                print("Invalid username or password!")
                return None
        except Exception as e:
            print(f"Error logging in: {e}")
            return None
    
    def login_admin(self, username, password):
        """Authenticate an admin"""
        try:
            hashed_password = self.hash_password(password)
            query = "SELECT * FROM admins WHERE username = %s AND password = %s"
            self.db.cursor.execute(query, (username, hashed_password))
            result = self.db.cursor.fetchone()
            
            if result:
                print(f"Admin '{username}' logged in successfully!")
                return {
                    "admin_id": result[0],
                    "name": result[1],
                    "username": result[2],
                    "email": result[4],
                    "phone": result[5],
                    "role": result[6]
                }
            else:
                print("Invalid username or password!")
                return None
        except Exception as e:
            print(f"Error logging in: {e}")
            return None


# Create a single auth instance to be shared across the application
auth = Auth()
