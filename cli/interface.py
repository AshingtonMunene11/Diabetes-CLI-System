#add-patient
#Prompt for glucose reading and patient ID
#add-medication
#Show average glucose, current meds, and recent logs for a patient

import click
from sqlalchemy.exc import SQLAlchemyError
from db.setup import Session
from models.patient import Patient
from models.glucose_log import GlucoseLog
from models.medication import Medication
from tabulate import tabulate
from datetime import datetime, date


def _print_table(rows, headers):
    click.echo(tabulate(rows, headers=headers, tablefmt="fancy_grid"))


def _parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Diabetes Management CLI"""
    if ctx.invoked_subcommand is None:
        click.echo("Welcome to the Diabetes CLI System!")
        while True:
            click.echo("\nSelect an option:")
            options = [
                "Patients",
                "Glucose Logs",
                "Medications",
                "Exit",
            ]
            for i, label in enumerate(options, start=1):
                click.echo(f"{i}. {label}")
            choice = click.prompt("Enter choice number", type=int)
            if choice == 1:
                _patients_menu()
            elif choice == 2:
                _glucose_menu()
            elif choice == 3:
                _medications_menu()
            elif choice == 4:
                click.echo("Thank you for using the Diabetes CLI System!")
                break
            else:
                click.echo("Invalid choice. Choose amongst the options.")


def _patients_menu():
    session = Session()
    try:
        click.echo("\nPatients Menu:")
        click.echo("1. List all")
        click.echo("2. Create")
        click.echo("3. Delete")
        click.echo("4. Find by name")
        click.echo("5. View related (logs + medications)")
        action = click.prompt("Enter choice number", type=int)
        if action == 1:
            patients = Patient.get_all(session)
            if not patients:
                click.echo("No patients found.")
                return
            rows = [[p.id, p.name, p.date_of_birth.strftime("%Y-%m-%d"), p.contact, p.age, p.average_glucose] for p in patients]
            _print_table(rows, ["ID", "Name", "DOB", "Contact", "Age", "Avg Glucose"])
        elif action == 2:
            name = click.prompt("Name")
            dob_str = click.prompt("DOB (YYYY-MM-DD)")
            contact = click.prompt("Contact", default="")
            dob = _parse_date(dob_str)
            p = Patient.create(session, name=name, date_of_birth=dob, contact=contact)
            click.echo(f"Created patient {p.id}: {p.name}")
            # Optional initial glucose reading
            if click.confirm("Log an initial glucose reading now?", default=False):
                reading = click.prompt("Reading (mg/dL)", type=float)
                if reading <= 0:
                    click.echo("Reading must be positive. Skipping initial log.")
                else:
                    GlucoseLog.create(session, patient=p, reading=reading)
                    click.echo("Initial glucose logged.")
        elif action == 3:
            pid = click.prompt("Patient ID", type=int)
            p = Patient.get_by_id(session, pid)
            if not p:
                click.echo("Patient not found.")
                return
            p.delete(session)
            click.echo("Deleted.")
        elif action == 4:
            term = click.prompt("Search term (name)")
            matches = Patient.find_by_name(session, term)
            if not matches:
                click.echo("No matches.")
                return
            rows = [[p.id, p.name, p.date_of_birth.strftime("%Y-%m-%d"), p.contact] for p in matches]
            _print_table(rows, ["ID", "Name", "DOB", "Contact"])
        elif action == 5:
            pid = click.prompt("Patient ID", type=int)
            p = Patient.get_by_id(session, pid)
            if not p:
                click.echo("Patient not found.")
                return
            click.echo(f"\nPatient: {p.name} (Age {p.age})  Avg Glucose: {p.average_glucose}")
            logs = p.glucose_logs
            meds = p.medications
            if logs:
                rows = [[g.id, g.reading, g.timestamp.strftime("%Y-%m-%d %H:%M")] for g in logs]
                _print_table(rows, ["Log ID", "Reading", "Timestamp"])
            else:
                click.echo("No glucose logs.")
            if meds:
                rows = [[m.id, m.name, m.dosage, (m.start_date.strftime("%Y-%m-%d") if m.start_date else "-")] for m in meds]
                _print_table(rows, ["Med ID", "Name", "Dosage", "Start Date"])
            else:
                click.echo("No medications.")
        else:
            click.echo("Invalid choice.")
    except Exception as e:
        session.rollback()
        click.echo(f"Error: {e}")
    finally:
        session.close()


def _glucose_menu():
    session = Session()
    try:
        click.echo("\nGlucose Logs Menu:")
        click.echo("1. List all")
        click.echo("2. Create")
        click.echo("3. Delete")
        click.echo("4. Find by date range")
        click.echo("5. List by patient")
        action = click.prompt("Enter choice number", type=int)
        if action == 1:
            logs = GlucoseLog.get_all(session)
            if not logs:
                click.echo("No glucose logs found.")
                return
            rows = [[g.id, g.patient_id, g.reading, g.timestamp.strftime("%Y-%m-%d %H:%M")] for g in logs]
            _print_table(rows, ["ID", "Patient ID", "Reading", "Timestamp"])
        elif action == 2:
            pid = click.prompt("Patient ID", type=int)
            patient = Patient.get_by_id(session, pid)
            if not patient:
                click.echo("Patient not found.")
                return
            reading = click.prompt("Reading (mg/dL)", type=float)
            if reading <= 0:
                click.echo("Reading must be positive.")
                return
            GlucoseLog.create(session, patient=patient, reading=reading)
            click.echo("Logged.")
        elif action == 3:
            gid = click.prompt("Glucose Log ID", type=int)
            g = GlucoseLog.get_by_id(session, gid)
            if not g:
                click.echo("Log not found.")
                return
            g.delete(session)
            click.echo("Deleted.")
        elif action == 4:
            start = _parse_date(click.prompt("Start date (YYYY-MM-DD)"))
            end = _parse_date(click.prompt("End date (YYYY-MM-DD)"))
            logs = GlucoseLog.find_by_date_range(session, datetime.combine(start, datetime.min.time()), datetime.combine(end, datetime.max.time()))
            if not logs:
                click.echo("No logs in range.")
                return
            rows = [[g.id, g.patient_id, g.reading, g.timestamp.strftime("%Y-%m-%d %H:%M")] for g in logs]
            _print_table(rows, ["ID", "Patient ID", "Reading", "Timestamp"])
        elif action == 5:
            pid = click.prompt("Patient ID", type=int)
            logs = session.query(GlucoseLog).filter(GlucoseLog.patient_id == pid).all()
            if not logs:
                click.echo("No logs for patient.")
                return
            rows = [[g.id, g.reading, g.timestamp.strftime("%Y-%m-%d %H:%M")] for g in logs]
            _print_table(rows, ["Log ID", "Reading", "Timestamp"])
        else:
            click.echo("Invalid choice.")
    except Exception as e:
        session.rollback()
        click.echo(f"Error: {e}")
    finally:
        session.close()


def _medications_menu():
    session = Session()
    try:
        click.echo("\nMedications Menu:")
        click.echo("1. List all")
        click.echo("2. Create")
        click.echo("3. Delete")
        click.echo("4. List by patient")
        action = click.prompt("Enter choice number", type=int)
        if action == 1:
            meds = Medication.get_all(session)
            if not meds:
                click.echo("No medications found.")
                return
            rows = [[m.id, m.patient_id, m.name, m.dosage, (m.start_date.strftime("%Y-%m-%d") if m.start_date else "-")] for m in meds]
            _print_table(rows, ["ID", "Patient ID", "Name", "Dosage", "Start Date"])
        elif action == 2:
            pid = click.prompt("Patient ID", type=int)
            patient = Patient.get_by_id(session, pid)
            if not patient:
                click.echo("Patient not found.")
                return
            name = click.prompt("Medication name")
            dosage = click.prompt("Dosage", default="")
            start = click.prompt("Start date (YYYY-MM-DD)", default="")
            start_date = _parse_date(start) if start else None
            Medication.create(session, patient=patient, name=name, dosage=dosage, start_date=start_date)
            click.echo("Created medication.")
        elif action == 3:
            mid = click.prompt("Medication ID", type=int)
            m = Medication.get_by_id(session, mid)
            if not m:
                click.echo("Medication not found.")
                return
            m.delete(session)
            click.echo("Deleted.")
        elif action == 4:
            pid = click.prompt("Patient ID", type=int)
            meds = session.query(Medication).filter(Medication.patient_id == pid).all()
            if not meds:
                click.echo("No medications for patient.")
                return
            rows = [[m.id, m.name, m.dosage, (m.start_date.strftime("%Y-%m-%d") if m.start_date else "-")] for m in meds]
            _print_table(rows, ["Med ID", "Name", "Dosage", "Start Date"])
        else:
            click.echo("Invalid choice.")
    except Exception as e:
        session.rollback()
        click.echo(f"Error: {e}")
    finally:
        session.close()


@cli.command()
@click.option('--name', prompt='Patient name', help='Full name of the patient')
@click.option('--dob', prompt='Date of birth (YYYY-MM-DD)', help='Date of birth in YYYY-MM-DD format')
@click.option('--contact', prompt='Contact info', help='Phone or email')
def add_patient(name, dob, contact):
    """Add a new patient to the system."""
    session = Session()
    try:
        dob_parsed = datetime.strptime(dob, "%Y-%m-%d").date()
        new_patient = Patient(name=name, date_of_birth=dob_parsed, contact=contact)
        session.add(new_patient)
        session.commit()
        click.echo(f"✅ Patient '{name}' added successfully.")
      
        if click.confirm("Log an initial glucose reading now?", default=False):
            reading = click.prompt("Reading (mg/dL)", type=float)
            if reading <= 0:
                click.echo("Reading must be positive. Skipping initial log.")
            else:
                GlucoseLog.create(session, patient=new_patient, reading=reading)
                click.echo("Initial glucose logged.")
    except ValueError:
        click.echo("❌ Invalid date format. Please use YYYY-MM-DD.")
    except SQLAlchemyError as e:
        session.rollback()
        click.echo(f"❌ Database error: {e}")
    finally:
        session.close()


@cli.command()
@click.option('--patient-id', prompt='Patient ID', help='ID of the patient')
@click.option('--reading', prompt='Glucose reading (mg/dL)', type=float, help='Blood sugar level')
def log_glucose(patient_id, reading):
    """Log a glucose reading for a patient."""
    session = Session()
    try:
        patient = session.query(Patient).get(int(patient_id))
        if not patient:
            click.echo(f"❌ No patient found with ID {patient_id}")
            return

        new_log = GlucoseLog(reading=reading, patient=patient)
        session.add(new_log)
        session.commit()
        click.echo(f"✅ Glucose reading of {reading} mg/dL logged for {patient.name}")
    except SQLAlchemyError as e:
        session.rollback()
        click.echo(f"❌ Database error: {e}")
    finally:
        session.close()


@cli.command()
def view_patients():
    """Display all registered patients in a table."""
    session = Session()
    try:
        patients = session.query(Patient).all()
        if not patients:
            click.echo("⚠️ No patients found.")
            return

        table = [
            [p.id, p.name, p.date_of_birth.strftime("%Y-%m-%d"), p.contact]
            for p in patients
        ]
        headers = ["ID", "Name", "Date of Birth", "Contact"]
        click.echo(tabulate(table, headers=headers, tablefmt="fancy_grid"))
    except SQLAlchemyError as e:
        click.echo(f"❌ Database error: {e}")
    finally:
        session.close()