from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Union
import sqlite3
# Baseclass and Classes
from classes_1 import (
    Base,
    Account,
    Payment,
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

# Function for adding content to the tables
def add_content(session, condition:str, **kwargs: Union[str, int, float, list, dict, bool]):
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
    try:
        match condition:
            case 'users':
                add_user(session, **kwargs)
            case 'main_users':
                add_main_user(session, **kwargs)
            case 'other_users':
                add_other_user(session, **kwargs)
            case 'subscriptions':
                add_subscription(session, **kwargs)
            case 'reviews':
                add_review(session, **kwargs)
            case 'cast':
                add_cast(session, **kwargs)
            case 'directors':
                add_director(session, **kwargs)
            case 'actors':
                add_actor(session, **kwargs)
            case 'media':
                add_media(session, **kwargs)
            case 'movie':
                add_movie(session, **kwargs)
            case 'series':
                add_series(session, **kwargs)
            case 'episodes':
                add_episode(session, **kwargs)
            case 'watchlists':
                add_watchlist(session, **kwargs)
            case _:
                raise ValueError(f"Invalid condition '{condition}' specified for content insertion.")
    
    except Exception as e:
        print(f"Error occurred: {e}")
        raise 


# Function for removing content from the tables
def remove_content(session, condition:str, id:int):
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
        case 'users':
            remove_user(session, id)
        case 'main_users':
            remove_main_user(session, id)
        case 'other_users':
            remove_other_user(session, id)
        case 'subscriptions':
            remove_subscription(session, id)
        case 'reviews':
            remove_review(session, id)
        case 'cast':
            remove_cast(session, id)
        case 'directors':
            remove_director(session, id)
        case 'actors':
            remove_actor(session, id)
        case 'media':
            remove_media(session, id)
        case 'movie':
            remove_movie(session, id)
        case 'series':
            remove_series(session, id)
        case 'episodes':
            remove_episode(session, id)
        case 'watchlists':
            remove_watchlist(session, id)
        case _:
            raise ValueError(f"Invalid condition '{condition}' specified for content removal.")

# Instance functions     
def add_user(session, **kwargs):
    user = User(**kwargs)
    session.add(user)
    session.commit()

def add_main_user(session, **kwargs):
    main_user = MainUser(**kwargs)
    session.add(main_user)
    session.commit()

def add_other_user(session, **kwargs):
    other_user = OtherUser(**kwargs)
    session.add(other_user)
    session.commit()

def add_subscription(session, **kwargs):
    subscription = Subscription(**kwargs)
    session.add(subscription)
    session.commit()

def add_review(session, **kwargs):
    review = Review(**kwargs)
    session.add(review)
    session.commit()

def add_cast(session, **kwargs):
    cast = Cast(**kwargs)
    session.add(cast)
    session.commit()

def add_director(session, **kwargs):
    director = Director(**kwargs)
    session.add(director)
    session.commit()

def add_actor(session, **kwargs):
    actor = Actor(**kwargs)
    session.add(actor)
    session.commit()

def add_media(session, **kwargs):
    media = Media(**kwargs)
    session.add(media)
    session.commit()

def add_movie(session, **kwargs):
    movie = Movie(**kwargs)
    session.add(movie)
    session.commit()

def add_series(session, **kwargs):
    series = Series(**kwargs)
    session.add(series)
    session.commit()

def add_episode(session, **kwargs):
    episode = Episode(**kwargs)
    session.add(episode)
    session.commit()

def add_watchlist(session, **kwargs):
    watchlist = Watchlist(**kwargs)
    session.add(watchlist)
    session.commit()


# Remove functions
def remove_user(session, id:int):
    user = session.query(User).get(id)
    if user:
        session.delete(user)
        session.commit()

def remove_main_user(session, id:int):
    main_user = session.query(MainUser).get(id)
    if main_user:
        session.delete(main_user)
        session.commit()

def remove_other_user(session, id:int):
    other_user = session.query(OtherUser).get(id)
    if other_user:
        session.delete(other_user)
        session.commit()

def remove_subscription(session, id:int):
    subscription = session.query(Subscription).get(id)
    if subscription:
        session.delete(subscription)
        session.commit()

def remove_review(session, id:int):
    review = session.query(Review).get(id)
    if review:
        session.delete(review)
        session.commit()

def remove_cast(session, id:int):
    cast = session.query(Cast).get(id)
    if cast:
        session.delete(cast)
        session.commit()

def remove_director(session, id:int):
    director = session.query(Director).get(id)
    if director:
        session.delete(director)
        session.commit()

def remove_actor(session, id:int):
    actor = session.query(Actor).get(id)
    if actor:
        session.delete(actor)
        session.commit()

def remove_media(session, id:int):
    media = session.query(Media).get(id)
    if media:
        session.delete(media)
        session.commit()

def remove_movie(session, id:int):
    movie = session.query(Movie).get(id)
    if movie:
        session.delete(movie)
        session.commit()

def remove_series(session, id:int):
    series = session.query(Series).get(id)
    if series:
        session.delete(series)
        session.commit()

def remove_episode(session, id:int):
    episode = session.query(Episode).get(id)
    if episode:
        session.delete(episode)
        session.commit()

def remove_watchlist(session, id:int):
    watchlist = session.query(Watchlist).get(id)
    if watchlist:
        session.delete(watchlist)
        session.commit()
