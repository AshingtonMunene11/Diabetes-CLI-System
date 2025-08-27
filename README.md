# Diabetes CLI System

A simple command-line app to manage patients, glucose logs, and medications using SQLAlchemy and Click.

## Setup

1. Install Python 3.8+
2. Install dependencies with Pipenv:
   
   ```bash
   pipenv install
   pipenv shell
   ```
3. Optional: set a custom database URL in a `.env` file:
   
   ```
   DATABASE_URL=sqlite:///diabetes.db
   ```

## Running

```bash
python main.py
```

The app auto-creates tables on startup. You can also run subcommands directly:

```bash
python main.py add-patient
python main.py log-glucose
python main.py view_patients
```

## CLI Menus

- Patients: list/create/delete/find/view-related
- Glucose Logs: list/create/delete/find-by-date-range/list-by-patient
- Medications: list/create/delete/list-by-patient

## Data Model

- Patient 1—* GlucoseLog
- Patient 1—* Medication

Key fields:
- Patient: `name` (required), `date_of_birth` (required), `contact`
- GlucoseLog: `reading` (>0), `timestamp` (default now), `patient_id`
- Medication: `name` (required), `dosage`, `start_date`, `patient_id`

Computed properties:
- Patient.age — derived from `date_of_birth`
- Patient.average_glucose — average of related `GlucoseLog.reading`

## Examples

- Create a patient: follow prompts in Patients → Create
- Log glucose: Glucose Logs → Create
- View a patient’s related data: Patients → View related

## Development

- Tests can be added with `pytest`
- DB schema is created via `Base.metadata.create_all(engine)` on app start