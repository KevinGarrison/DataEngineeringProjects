from sqlalchemy import create_engine, inspect, MetaData
from sqlalchemy.orm import sessionmaker
import sqlite3

from classes import Base


def setup(database_name:str):
    '''
    Initializes a SQLite database and returns a session to interact with it.

    Parameters:
    ----------
    database_name : str
        The name of the SQLite database file (e.g., 'example.db').
    
    Returns:
    -------
    session : Session
        A session object that allows interaction with the database.
    '''
    sqlite3.connect(f'{database_name}')
    engine = create_engine(f'sqlite:///{database_name}')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session, engine

def drop_all_tables(engine):
    """
    Drops all tables in the provided SQLAlchemy engine and verifies deletion.
    
    Parameters:
    - engine: SQLAlchemy engine instance connected to the target database.
    
    Returns:
    - str: Message confirming whether all tables were deleted or if any remain.
    """
    # Reflect and drop all tables
    metadata = MetaData()
    metadata.reflect(bind=engine)
    metadata.drop_all(bind=engine)
    
    # Verify if tables have been deleted
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    if not tables:
        return "All tables have been successfully deleted."
    else:
        return f"Some tables still exist: {tables}"

