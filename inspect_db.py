from db.setup import engine
from sqlalchemy import inspect

def inspect_database():
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if tables:
        print("📋 Tables found in the database:")
        for table in tables:
            print(f" - {table}")
    else:
        print("⚠️ No tables found. You may need to run Base.metadata.create_all(engine).")

if __name__ == "__main__":
    inspect_database()
