from cli.interface import cli
from db.setup import Base, engine

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    cli()
