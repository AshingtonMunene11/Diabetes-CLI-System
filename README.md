# Diabetes CLI System

A command‑line app for managing patients, glucose logs, and medications using SQLAlchemy and Click. It demonstrates clean CLI design, ORM relationships, computed properties, and optional data seeding.

## Contents
- Overview
- Requirements
- Quick start
- Configuration
- Database and migrations (Alembic)
- Seeding demo data
- CLI usage and commands
- Data model and constraints
- Examples
- Testing
- Troubleshooting

## Overview
This CLI lets you:
- Create, list, find, and delete Patients
- Log, list, filter by date, and delete Glucose Logs
- Create, list, list-by-patient, and delete Medications
- View a Patient’s related Glucose Logs and Medications

## Requirements
- Python 3.8+
- Pipenv

## Quick start
```bash
cd /root/phase-3/development/finalProject/Diabetes-CLI-System
pipenv install
pipenv shell
python main.py
```
On first run, the app will create the SQLite database if needed. You’ll see a persistent menu with Patients, Glucose Logs, and Medications.

## Configuration
- Environment variables are loaded from `.env` if present.
- Database URL (optional):
  ```
  DATABASE_URL=sqlite:///diabetes.db
  ```
- Default DB: `sqlite:///diabetes.db` in the project root.

## Database and migrations (Alembic)
This project includes Alembic to manage schema migrations. Typical workflow:
```bash
# Create an empty baseline revision (optional but recommended)
pipenv run alembic revision -m "baseline"

# Autogenerate a migration from model metadata
pipenv run alembic revision --autogenerate -m "create tables"

# Apply latest migrations
pipenv run alembic upgrade head
```
Notes:
- The Alembic config reads `DATABASE_URL` from environment when running migrations.
- You can continue to use `sqlite:///diabetes.db` locally.

## Seeding demo data
A script is provided to populate demo data (5 patients, each with logs and at least one medication). It DROPS and recreates tables.
```bash
pipenv shell
python data/seed_data.py
```
Verify:
```bash
python inspect_db.py
python main.py   # Patients → View related
```

## CLI usage and commands
Start the CLI:
```bash
python main.py
```
Main menu:
- Patients: list/create/delete/find/view-related
- Glucose Logs: list/create/delete/find-by-date-range/list-by-patient
- Medications: list/create/delete/list-by-patient
- Exit

You can also call some commands directly:
```bash
python main.py add-patient
python main.py log-glucose
python main.py view_patients
```

### Patients
- Create: prompts Name, DOB (YYYY-MM-DD), Contact. Then optionally offers to log an initial glucose reading.
- List all: shows ID, Name, DOB, Contact, Age, Avg Glucose.
- Find by name: case-insensitive search.
- Delete: deletes the patient and related logs/meds (cascade delete).
- View related: displays a patient’s logs and medications.

### Glucose Logs
- Create: requires Patient ID and Reading (mg/dL).
- List all: shows all logs.
- Find by date range: filter by start/end date.
- List by patient: show logs for a patient.
- Delete: remove a specific log by ID.

### Medications
- Create: requires Patient ID, Name, optional Dosage, optional Start date.
- List all: shows all medications.
- List by patient: show medications for a patient.
- Delete: remove a specific medication by ID.

## Data model and constraints
- Patient (`patients`)
  - id (PK)
  - name (required; non-empty)
  - date_of_birth (required)
  - contact (optional)
  - Relationships: `glucose_logs` (1‑*), `medications` (1‑*)
  - Computed properties: `age`, `average_glucose`
- GlucoseLog (`glucose_logs`)
  - id (PK)
  - reading (required; > 0)
  - timestamp (defaults to now)
  - patient_id (FK to patients.id, required)
- Medication (`medications`)
  - id (PK)
  - name (required; non-empty)
  - dosage (optional)
  - start_date (optional)
  - patient_id (FK to patients.id, required)

## Examples
Run the app and add a patient, then log initial glucose when prompted:
```text
Patients → Create
Name: Jane Doe
DOB (YYYY-MM-DD): 1990-01-01
Contact: jane@example.com
Log an initial glucose reading now? [y/N]: y
Reading (mg/dL): 120
```
View related data for that patient:
```text
Patients → View related → Patient ID: <id>
```

## Testing
- Quick manual checks:
  - `python inspect_db.py` to list tables
  - `python main.py` to exercise menus
- You can add `pytest` tests under `tests/` to exercise model methods (e.g., `create`, `get_by_id`, `find_by_*`).

## Troubleshooting
- “alembic could not be found”: ensure Alembic is installed (it is in Pipfile) and use `pipenv run alembic ...`.
- Import errors when running `data/seed_data.py`: run from the project root; the script adjusts `sys.path` automatically.
- Old data still showing: reseed or delete `diabetes.db` and run the seeder again.
- Invalid date errors: enter dates as `YYYY-MM-DD`.

## License
© 2025 Ashington Munene — Moringa School.


