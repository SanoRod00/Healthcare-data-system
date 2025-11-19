import sqlite3
import getpass
import datetime
import os
from typing import Optional

DB_PATH = "healthcare.db"


# ------------------------------
# DATABASE CONNECTION
# ------------------------------
def get_conn():
    return sqlite3.connect(DB_PATH)


# ------------------------------
# INITIALIZE DATABASE
# ------------------------------
def init_db():
    if os.path.exists(DB_PATH):
        return

    conn = get_conn()
    c = conn.cursor()

    # USERS
    c.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'doctor', 'patient')),
            full_name TEXT
        )
    ''')

    # PATIENTS
    c.execute('''
        CREATE TABLE patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            dob TEXT,
            gender TEXT,
            contact TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # DOCTORS
    c.execute('''
        CREATE TABLE doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            specialization TEXT,
            contact TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # APPOINTMENTS
    c.execute('''
        CREATE TABLE appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            scheduled_at TEXT NOT NULL,
            reason TEXT,
            status TEXT NOT NULL DEFAULT 'scheduled',
            FOREIGN KEY(patient_id) REFERENCES patients(id),
            FOREIGN KEY(doctor_id) REFERENCES doctors(id)
        )
    ''')

    # HEALTH LOGS
    c.execute('''
        CREATE TABLE health_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            recorded_by INTEGER,
            recorded_at TEXT NOT NULL,
            notes TEXT,
            temperature REAL,
            pulse INTEGER,
            blood_pressure TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(id),
            FOREIGN KEY(recorded_by) REFERENCES users(id)
        )
    ''')

    # PRESCRIPTIONS
    c.execute('''
        CREATE TABLE prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            prescribed_at TEXT NOT NULL,
            medication TEXT NOT NULL,
            dosage TEXT NOT NULL,
            notes TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(id),
            FOREIGN KEY(doctor_id) REFERENCES doctors(id)
        )
    ''')

    # LAB TESTS
    c.execute('''
        CREATE TABLE lab_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            ordered_at TEXT NOT NULL,
            test_type TEXT NOT NULL,
            results TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            FOREIGN KEY(patient_id) REFERENCES patients(id),
            FOREIGN KEY(doctor_id) REFERENCES doctors(id)
        )
    ''')

    conn.commit()

    # DEFAULT USERS
    c.execute("""
        INSERT INTO users (username, password, role, full_name)
        VALUES 
        ('admin', 'adminpass', 'admin', 'System Admin'),
        ('dr_smith', 'docpass', 'doctor', 'Dr. Smith'),
        ('john_doe', 'patientpass', 'patient', 'John Doe')
    """)
    conn.commit()

    # create default doctor/patient profiles
    c.execute("INSERT INTO doctors (user_id, specialization, contact) VALUES (2, 'General Medicine', '0788001122')")
    c.execute("INSERT INTO patients (user_id, dob, gender, contact) VALUES (3, '1990-01-01', 'M', '0788003344')")
    conn.commit()

    conn.close()
    print("Database initialized with default admin/doctor/patient.")


# ----------------------------------------------------------
# USER REGISTRATION
# ----------------------------------------------------------
def register_user(username: str, password: str, role: str, full_name: str) -> Optional[int]:
    conn = get_conn()
    c = conn.cursor()

    try:
        c.execute(
            "INSERT INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)",
            (username, password, role, full_name)
        )
        conn.commit()

        user_id = c.lastrowid

        if role == "patient":
            c.execute("INSERT INTO patients (user_id) VALUES (?)", (user_id,))
        elif role == "doctor":
            c.execute("INSERT INTO doctors (user_id) VALUES (?)", (user_id,))

        conn.commit()
        return user_id

    except sqlite3.IntegrityError:
        return None

    finally:
        conn.close()


# ----------------------------------------------------------
# LOGIN
# ----------------------------------------------------------
def authenticate(username: str, password: str) -> Optional[dict]:
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        SELECT id, username, role, full_name 
        FROM users 
        WHERE username = ? AND password = ?
    """, (username, password))

    row = c.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "username": row[1],
            "role": row[2],
            "full_name": row[3]
        }
    return None


# ----------------------------------------------------------
# PATIENT FUNCTIONS
# ----------------------------------------------------------
def get_patient_row_by_user_id(user_id: int):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        SELECT id, dob, gender, contact 
        FROM patients 
        WHERE user_id = ?
    """, (user_id,))

    row = c.fetchone()
    conn.close()
    return row


def patient_profile(user):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        SELECT id, dob, gender, contact
        FROM patients
        WHERE user_id = ?
    """, (user["id"],))

    row = c.fetchone()
    conn.close()

    if row:
        return {
            "patient_id": row[0],
            "dob": row[1],
            "gender": row[2],
            "contact": row[3]
        }
    return None


def get_patient_appointments(patient_id: int):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        SELECT a.id, a.scheduled_at, a.reason, d.specialization, d.contact
        FROM appointments a
        JOIN doctors d ON a.doctor_id = d.id
        WHERE a.patient_id = ?
    """, (patient_id,))

    rows = c.fetchall()
    conn.close()
    return rows


# ----------------------------------------------------------
# DOCTOR FUNCTIONS
# ----------------------------------------------------------
def doctor_profile(user):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        SELECT id, specialization, contact
        FROM doctors
        WHERE user_id = ?
    """, (user["id"],))

    row = c.fetchone()
    conn.close()

    if row:
        return {
            "doctor_id": row[0],
            "specialization": row[1],
            "contact": row[2]
        }
    return None


def doctor_get_appointments(doctor_id: int):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        SELECT a.id, a.scheduled_at, a.reason, p.gender, p.contact
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        WHERE a.doctor_id = ?
    """, (doctor_id,))

    rows = c.fetchall()
    conn.close()
    return rows


# ----------------------------------------------------------
# LOGIN HANDLER
# ----------------------------------------------------------
def login():
    print("\n====== LOGIN ======")
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    user = authenticate(username, password)

    if user:
        print("\nLogin Successful!\n")
        return user

    print("\nInvalid credentials\n")
    return None


# ----------------------------------------------------------
# PATIENT DASHBOARD
# ----------------------------------------------------------
def patient_dashboard(user):
    profile = patient_profile(user)

    if profile is None:
        print("No patient profile found.")
        return

    while True:
        print(f"""
===== PATIENT DASHBOARD =====
1. View Profile
2. View Appointments
3. Logout
""")

        choice = input("Choose: ")

        if choice == "1":
            print("\n--- PROFILE ---")
            print(f"DOB: {profile['dob']}")
            print(f"Gender: {profile['gender']}")
            print(f"Contact: {profile['contact']}\n")

        elif choice == "2":
            appointments = get_patient_appointments(profile["patient_id"])

            if not appointments:
                print("\nNo appointments found.\n")
            else:
                print("\n--- APPOINTMENTS ---")
                for a in appointments:
                    print(f"ID: {a[0]} | When: {a[1]} | Reason: {a[2]} | Doctor: {a[3]} | Contact: {a[4]}")
                print()

        elif choice == "3":
            print("Logging out...\n")
            break

        else:
            print("Invalid option\n")


# ----------------------------------------------------------
# DOCTOR DASHBOARD
# ----------------------------------------------------------
def doctor_dashboard(user):
    profile = doctor_profile(user)

    if profile is None:
        print("No doctor profile found.")
        return

    while True:
        print(f"""
===== DOCTOR DASHBOARD =====
1. View Profile
2. View Appointments
3. Logout
""")

        choice = input("Choose: ")

        if choice == "1":
            print("\n--- PROFILE ---")
            print(f"Specialization: {profile['specialization']}")
            print(f"Contact: {profile['contact']}\n")

        elif choice == "2":
            appointments = doctor_get_appointments(profile["doctor_id"])

            if not appointments:
                print("\nNo appointments found.\n")
            else:
                print("\n--- APPOINTMENTS ---")
                for a in appointments:
                    print(f"ID: {a[0]} | When: {a[1]} | Reason: {a[2]} | Patient Gender: {a[3]} | Contact: {a[4]}")
                print()

        elif choice == "3":
            print("Logging out...\n")
            break

        else:
            print("Invalid option\n")
