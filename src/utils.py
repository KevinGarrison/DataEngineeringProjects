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
    session = Session()
    return session, engine


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
        case 'accounts':
            add_account(kwargs)
        case 'payments':
            add_payment(kwargs)
        case 'users':
            add_user(kwargs)
        case 'main_users':
            add_main_user(kwargs)
        case 'other_users':
            add_other_user(kwargs)
        case 'subscriptions':
            add_subscription(kwargs)
        case 'reviews':
            add_review(kwargs)
        case 'cast':
            add_cast(kwargs)
        case 'directors':
            add_director(kwargs)
        case 'actors':
            add_actor(kwargs)
        case 'media':
            add_media(kwargs)
        case 'movie':
            add_movie(kwargs)
        case 'series':
            add_series(kwargs)
        case 'episodes':
            add_episode(kwargs)
        case 'watchlists':
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
        case 'accounts':
            remove_account(kwargs)
        case 'payments':
            remove_payment(kwargs)
        case 'users':
            remove_user(kwargs)
        case 'main_users':
            remove_main_user(kwargs)
        case 'other_users':
            remove_other_user(kwargs)
        case 'subscriptions':
            remove_subscription(kwargs)
        case 'reviews':
            remove_review(kwargs)
        case 'cast':
            remove_cast(kwargs)
        case 'directors':
            remove_director(kwargs)
        case 'actors':
            remove_actor(kwargs)
        case 'media':
            remove_media(kwargs)
        case 'movie':
            remove_movie(kwargs)
        case 'series':
            remove_series(kwargs)
        case 'episodes':
            remove_episode(kwargs)
        case 'watchlists':
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





