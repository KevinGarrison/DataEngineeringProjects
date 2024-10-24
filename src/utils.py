from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from classes import Base, alle Classes
import sqlite3

# Setup Database and Sessionmaker 
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
    #Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session(), engine

def add_content():
    pass

def add_genre():
    pass

def add_movie():
    pass

def add_series():
    pass

def add_episode():
    pass




