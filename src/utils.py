from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Union
import sqlite3
# Baseclass and Classes
from new_classes import (
    Base,
    User,
    MainUser,
    OtherUser,
    Subscription,
    Review,
    Cast,
    Director,
    Actor,
    Media,
    Movie,
    Series,
    Episode,
    Watchlist,
)


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
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session, engine


