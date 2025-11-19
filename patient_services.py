#!/bin/bash
import sqlite3
from datetime import datetime

class PatientSystem:
    def __init__(self):
        self.conn = sqlite3.connect('healthcare.db')
        self.create_tables()

    def create_tables(self):
        """Create necessary tables if they don't exist"""
        cursor = self.conn.cursor()

        # Patients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                contact TEXT,
                medical_history TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Health logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS health_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                blood_pressure TEXT,
                heart_rate INTEGER,
                temperature REAL,
                symptoms TEXT,
                log_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients (id)
            )
        ''')

        self.conn.commit()

    def register_patient(self):
        """Register a new patient"""
        print("\n=== PATIENT REGISTRATION ===")

        name = input("Enter patient name: ")
        age = int(input("Enter age: "))
        gender = input("Enter gender (M/F): ")
        contact = input("Enter contact number: ")
        medical_history = input("Enter medical history: ")

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO patients (name, age, gender, contact, medical_history)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, age, gender, contact, medical_history))

        self.conn.commit()
        patient_id = cursor.lastrowid

        print(f"\ Patient registered successfully!")
        print(f"Patient ID: {patient_id}")
        return patient_id

    def track_health(self, patient_id):
        """Track patient health data"""
        print("\n=== HEALTH TRACKING ===")

        blood_pressure = input("Enter blood pressure (e.g., 120/80): ")
        heart_rate = int(input("Enter heart rate: "))
        temperature = float(input("Enter temperature in °C: "))
        symptoms = input("Enter symptoms: ")

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO health_logs (patient_id, blood_pressure, heart_rate, temperature, symptoms)
            VALUES (?, ?, ?, ?, ?)
        ''', (patient_id, blood_pressure, heart_rate, temperature, symptoms))

        self.conn.commit()
        print(" Health data recorded successfully!")

    def view_health_history(self, patient_id):
        """View patient's health history"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT log_date, blood_pressure, heart_rate, temperature, symptoms
            FROM health_logs
            WHERE patient_id = ?
            ORDER BY log_date DESC
        ''', (patient_id,))

        records = cursor.fetchall()

        print("\n=== HEALTH HISTORY ===")
        if not records:
            print("No health records found.")
            return

        for record in records:
            print(f"Date: {record[0]}")
            print(f"Blood Pressure: {record[1]}")
            print(f"Heart Rate: {record[2]} bpm")
            print(f"Temperature: {record[3]}°C")
            print(f"Symptoms: {record[4]}")
            print("-" * 30)

    def search_patient(self):
        """Search for a patient by ID or name"""
        print("\n=== SEARCH PATIENT ===")
        search_term = input("Enter patient ID or name: ")

        cursor = self.conn.cursor()

        # Try searching by ID first
        if search_term.isdigit():
            cursor.execute('SELECT * FROM patients WHERE id = ?', (int(search_term),))
        else:
            cursor.execute('SELECT * FROM patients WHERE name LIKE ?', (f'%{search_term}%',))

        patients = cursor.fetchall()

        if not patients:
            print(" No patient found.")
            return None

        print("\n=== PATIENT FOUND ===")
        for patient in patients:
            print(f"ID: {patient[0]}")
            print(f"Name: {patient[1]}")
            print(f"Age: {patient[2]}")
            print(f"Gender: {patient[3]}")
            print(f"Contact: {patient[4]}")
            print(f"Medical History: {patient[5]}")
            print("-" * 30)

        return patients[0][0]  # Return first patient's ID

    def patient_dashboard(self):
        """Main patient dashboard"""
        while True:
            print("\n=== PATIENT DASHBOARD ===")
            print("1. Register New Patient")
            print("2. Search Patient")
            print("3. Track Health Data")
            print("4. View Health History")
            print("5. Exit")

            choice = input("\nEnter your choice (1-5): ")

            if choice == '1':
                self.register_patient()
            elif choice == '2':
                patient_id = self.search_patient()
                if patient_id:
                    # Show options for found patient
                    sub_choice = input("\n1. Track Health Data\n2. View Health History\nChoose: ")
                    if sub_choice == '1':
                        self.track_health(patient_id)
                    elif sub_choice == '2':
                        self.view_health_history(patient_id)
            elif choice == '3':
                patient_id = input("Enter patient ID: ")
                if patient_id.isdigit():
                    self.track_health(int(patient_id))
                else:
                    print(" Invalid patient ID")
            elif choice == '4':
                patient_id = input("Enter patient ID: ")
                if patient_id.isdigit():
                    self.view_health_history(int(patient_id))
                else:
                    print(" Invalid patient ID")
            elif choice == '5':
                print(" Thank you for using the Patient System!")
                break
            else:
                print(" Invalid choice. Please try again.")

# Main program
if __name__ == "__main__":
    system = PatientSystem()
    system.patient_dashboard()
