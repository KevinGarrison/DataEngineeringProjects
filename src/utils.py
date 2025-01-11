from sqlalchemy import create_engine, inspect, MetaData
from sqlalchemy.orm import sessionmaker
import sqlite3
import time
from neo4j import GraphDatabase


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


def neo4j_init(uri): # DONE
    """
    Initializes a connection to the Neo4j database.

    Args:
        uri (str): The URI of the Neo4j instance (default is "bolt://localhost:7687").
        user (str): The username for the Neo4j database (default is "neo4j").
        password (str): The password for the Neo4j database (default is "password").

    Returns:
        driver (neo4j.Driver): The Neo4j driver object.
    """
    try:
        # Create the driver
        driver = GraphDatabase.driver(uri)
        
        # Test the connection
        with driver.session() as session:
            session.run("RETURN 'Neo4j connection successful!' AS message")
        
        print("Neo4j connection initialized successfully.")
        return driver
    except Exception as e:
        print(f"Failed to initialize Neo4j connection: {e}")
        return None



def neo4j_add_relation_user_reviews(driver, user, reviews):
    pass

def neo4j_add_relation_user_watchlists(driver, user, watchlists):
    pass

def neo4j_add_relation_actor_movie_cast(driver, actor, movie, director):
    pass

def add_data_to_neo4j(driver, data)->bool:
    pass

def neo4j_close_sess(driver)->bool:
    pass

def query_1_neo4j(driver, query):
    '''
    print() für die query
    '''

def query_2_neo4j(driver, query):
   '''
    print() für die query
    '''

def query_3_neo4j(driver, query):
    '''
    print() für die query
    '''

    '''
    TODO:
    1. Funktionen implementieren
    3. Queries schreiben
    3. Doku in oveleaf

    '''

