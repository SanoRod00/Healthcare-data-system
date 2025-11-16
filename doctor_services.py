import datetime

def doctor_dashboard_menu():
    """Display the doctor dashboard menu and handle user choices."""
    while True:
        print("\n--- Doctor Dashboard ---")
        print("1. View my patients")
        print("2. Search patient by ID")
        print("3. View patient medical history")
        print("4. Record diagnosis / medical notes")
        print("5. Create a prescription")
        print("6. Order a lab test")
        print("7. View my upcoming appointments")
        print("8. Update appointment status")
        print("9. Log out")

        choice = input("Enter your choice (1-9): ").strip()
        if choice == "1":
            patients = view_patients()
            print("Patients:", patients)
        elif choice == "2":
            patient_id = input("Enter patient ID: ").strip()
            patient = get_patient_by_id(patient_id)
            print("Patient:", patient)
        elif choice == "3":
            patient_id = input("Enter patient ID: ").strip()
            history = view_medical_history(patient_id)
            print("Medical History:", history)
        elif choice == "4":
            patient_id = input("Enter patient ID: ").strip()
            notes = input("Enter diagnosis/notes: ").strip()
            result = add_medical_notes(patient_id, notes)
            print("Notes added:", result)
        elif choice == "5":
            patient_id = input("Enter patient ID: ").strip()
            prescription = create_prescription(patient_id)
            print("Prescription created:", prescription)
        elif choice == "6":
            patient_id = input("Enter patient ID: ").strip()
            lab_test = order_lab_test(patient_id)
            print("Lab test ordered:", lab_test)
        elif choice == "7":
            appointments = view_appointments()
            print("Appointments:", appointments)
        elif choice == "8":
            appointment_id = input("Enter appointment ID: ").strip()
            status = input("Enter new status (completed/rescheduled/cancelled): ").strip()
            result = update_appointment_status(appointment_id, status)
            print("Appointment updated:", result)
        elif choice == "9":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please select 1-9.")

def view_patients():
    """Return all patients assigned to the doctor."""
    # Placeholder for database query
    # TODO: Fetch patients assigned to current doctor from database
    patients = [
        {"id": "P001", "name": "John Doe", "age": 30},
        {"id": "P002", "name": "Jane Smith", "age": 25}
    ]
    return patients

def get_patient_by_id(patient_id):
    """Look up a patient using a unique ID."""
    # Placeholder for database query
    # TODO: Fetch patient by ID from database
    if patient_id == "P001":
        return {"id": "P001", "name": "John Doe", "age": 30, "contact": "john@example.com"}
    elif patient_id == "P002":
        return {"id": "P002", "name": "Jane Smith", "age": 25, "contact": "jane@example.com"}
    else:
        return None

def view_medical_history(patient_id):
    """Fetch health logs, prescriptions, lab results."""
    # Placeholder for database query
    # TODO: Fetch medical history from database
    history = {
        "patient_id": patient_id,
        "visits": [
            {"date": "2023-10-01", "diagnosis": "Flu", "notes": "Rest and fluids"},
            {"date": "2023-09-15", "diagnosis": "Checkup", "notes": "All good"}
        ],
        "prescriptions": [
            {"medicine": "Paracetamol", "dosage": "500mg", "duration": "5 days"}
        ],
        "lab_results": [
            {"test": "Blood Test", "result": "Normal", "date": "2023-10-02"}
        ]
    }
    return history

def add_medical_notes(patient_id, notes):
    """Add new diagnosis or notes for a patient."""
    # Placeholder for database insertion
    # TODO: Insert notes into database
    note_entry = {
        "patient_id": patient_id,
        "notes": notes,
        "date": datetime.datetime.now().isoformat(),
        "doctor_id": "D001"  # Current doctor
    }
    return note_entry

def create_prescription(patient_id):
    """Create a prescription for a patient."""
    medicine = input("Medicine name: ").strip()
    dosage = input("Dosage: ").strip()
    refills = input("Refills: ").strip()
    duration = input("Duration: ").strip()
    instructions = input("Instructions: ").strip()

    # Placeholder for database insertion
    # TODO: Insert prescription into database
    prescription = {
        "patient_id": patient_id,
        "medicine": medicine,
        "dosage": dosage,
        "refills": refills,
        "duration": duration,
        "instructions": instructions,
        "date": datetime.datetime.now().isoformat(),
        "doctor_id": "D001"
    }
    return prescription

def order_lab_test(patient_id):
    """Order a lab test for a patient."""
    test_type = input("Test type: ").strip()
    urgency = input("Urgency (routine/urgent): ").strip()
    notes = input("Notes: ").strip()

    # Placeholder for database insertion
    # TODO: Insert lab test order into database
    lab_test = {
        "patient_id": patient_id,
        "test_type": test_type,
        "urgency": urgency,
        "notes": notes,
        "date_ordered": datetime.datetime.now().isoformat(),
        "doctor_id": "D001"
    }
    return lab_test

def view_appointments():
    """List upcoming appointments for the doctor."""
    # Placeholder for database query
    # TODO: Fetch appointments for current doctor from database
    appointments = [
        {"id": "A001", "patient_id": "P001", "date": "2023-10-15", "time": "10:00", "status": "scheduled"},
        {"id": "A002", "patient_id": "P002", "date": "2023-10-16", "time": "14:00", "status": "scheduled"}
    ]
    return appointments

def update_appointment_status(appointment_id, status):
    """Update the status of an appointment."""
    # Placeholder for database update
    # TODO: Update appointment status in database
    if status in ["completed", "rescheduled", "cancelled"]:
        updated_appointment = {
            "id": appointment_id,
            "status": status,
            "updated_at": datetime.datetime.now().isoformat()
        }
        return updated_appointment
    else:
        raise ValueError("Invalid status.")
