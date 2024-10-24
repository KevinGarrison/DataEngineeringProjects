from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from classes import Base 
from typing import Union
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
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session(), engine


def add_content(condition:str, **kwargs: Union[str, int, float, list, dict, bool]):
    '''
    Adds content to the SQLite database. 
    Calls the individual functions for adding content. 

    Parameters:
    ----------
    condition : str
        The name of the table (e.g., 'ACCOUNT').
    
    **kwargs : str or int or float or list or dict or bool
        Variable length keyword arguments representing column names and their respective values.
        This allows for dynamic insertion of data into the specified table.
        The values can be of different types, such as:
        - str: String values for text fields.
        - int: Integer values for numeric fields.
        - float: Floating-point numbers for decimal fields.
        - list: List of values (if applicable).
        - dict: A dictionary of key-value pairs if multiple columns need to be populated.
        - bool: Boolean values for binary fields.

    Example:
    --------
    add_content_to_database('ACCOUNT', username='johndoe', age=28, balance=1000.50)
    '''
    match condition:
        case '':
            add_account(kwargs)
        case '':
            add_payment(kwargs)
        case '':
            add_user(kwargs)
        case '':
            add_main_user(kwargs)
        case '':
            add_other_user(kwargs)
        case '':
            add_subscription(kwargs)
        case '':
            add_review(kwargs)
        case '':
            add_cast(kwargs)
        case '':
            add_director(kwargs)
        case '':
            add_actor(kwargs)
        case '':
            add_media(kwargs)
        case '':
            add_movie(kwargs)
        case '':
            add_series(kwargs)
        case '':
            add_episode(kwargs)
        case '':
            add_watchlist(kwargs)

def remove_content(condition:str, **kwargs: Union[str, int, float, list, dict, bool]):
    '''
    Removes content from the SQLite database.
    Calls the individual functions for removing content. 
    
    Parameters:
    ----------
    condition : str
        The name of the table (e.g., 'ACCOUNT').

    **kwargs : str or int
        Variable length keyword arguments representing the conditions for removal.
        This allows for dynamic specification of which records to delete based on column values.
        The values can be of different types, such as:
        - str: String values for text fields.
        - int: Integer values for numeric fields.

    Example:
    --------
    remove_content_from_database('ACCOUNT', username='johndoe', age=28)
    '''
    match condition:
        case '':
            remove_account(kwargs)
        case '':
            remove_payment(kwargs)
        case '':
            remove_user(kwargs)
        case '':
            remove_main_user(kwargs)
        case '':
            remove_other_user(kwargs)
        case '':
            remove_subscription(kwargs)
        case '':
            remove_review(kwargs)
        case '':
            remove_cast(kwargs)
        case '':
            remove_director(kwargs)
        case '':
            remove_actor(kwargs)
        case '':
            remove_media(kwargs)
        case '':
            remove_movie(kwargs)
        case '':
            remove_series(kwargs)
        case '':
            remove_episode(kwargs)
        case '':
            remove_watchlist(kwargs)

def add_account():
    pass

def add_payment():
    pass

def add_user():
    pass

def add_main_user():
    pass

def add_other_user():
    pass

def add_subscription():
    pass

def add_review():
    pass

def add_cast():
    pass

def add_director():
    pass

def add_actor():
    pass

def add_media():
    pass

def add_movie():
    pass

def add_series():
    pass

def add_episode():
    pass

def add_watchlist():
    pass


def remove_account():
    pass

def remove_payment():
    pass

def remove_user():
    pass

def remove_main_user():
    pass

def remove_other_user():
    pass

def remove_subscription():
    pass

def remove_review():
    pass

def remove_cast():
    pass

def remove_director():
    pass

def remove_actor():
    pass

def remove_media():
    pass

def remove_movie():
    pass

def remove_series():
    pass

def remove_episode():
    pass

def remove_watchlist():
    pass





