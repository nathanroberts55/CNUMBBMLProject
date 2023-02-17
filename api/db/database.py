from sqlmodel import SQLModel, create_engine
from .models import *
# UIsing SQLite here but can easily use PostgreSQL by changing the url
sqlite_file_name = "stats.sqlite3"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# The engine is the interface to our database so we can execute SQL commands
engine = create_engine(sqlite_url, echo=True)


# using the engine we create the tables we need if they aren't already done
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    

if __name__ == '__main__':
    # creates the table if this file is run independently, as a script
    create_db_and_tables()