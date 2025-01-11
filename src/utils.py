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

def neo4j_add_relation_user_review_movie(driver):
    """
    Adds a user and their reviews linked to movies in the Neo4j database.

    Args:
        driver (neo4j.Driver): The Neo4j driver object.
    """
    user = {"user_id": 1, "name": "John Doe", "email": "johndoe@example.com"}
    reviews = [
        {"review_id": 101, "movie_id": 1, "rating": 9},
        {"review_id": 102, "movie_id": 2, "rating": 8}
    ]

    # Create or Merge User Node
    user_query = f"""
    MERGE (:User {{user_id: {user['user_id']}, name: '{user['name']}', email: '{user['email']}'}})
    """

    # Create Review Nodes and Link to Movies
    review_queries = []
    for review in reviews:
        review_queries.append(f"""
        MATCH (m:Movie {{id: {review['movie_id']}}})
        MERGE (r:Review {{review_id: {review['review_id']}, rating: {review['rating']}}})
        MERGE (r)-[:REVIEWS]->(m)
        MERGE (:User {{user_id: {user['user_id']}}})-[:REVIEWS]->(r)
        """)

    with driver.session() as session:
        # Create or Merge User Node
        session.run(user_query)

        # Create Reviews and Relationships
        for query in review_queries:
            session.run(query)

    print("User, their reviews, and links to movies have been added to the Neo4j database.")

def neo4j_add_relation_user_watchlists(driver):
    """
    Adds a user and their watchlists to the Neo4j database.

    Args:
        driver (neo4j.Driver): The Neo4j driver object.
    """
    user = {"user_id": 1, "name": "John Doe", "email": "johndoe@example.com"}
    watchlists = [
        {"watch_id": 201, "movie_id": 1},
        {"watch_id": 202, "movie_id": 2}
    ]

    user_query = f"""
    MERGE (:User {{user_id: {user['user_id']}, name: '{user['name']}', email: '{user['email']}'}})
    """

    watchlist_queries = []
    for watchlist in watchlists:
        watchlist_queries.append(f"""
        MATCH (u:User {{user_id: {user['user_id']}}}), (m:Movie {{id: {watchlist['movie_id']}}})
        CREATE (:Watchlist {{watch_id: {watchlist['watch_id']}}})-[:WATCHED_BY]->(u)-[:WATCHLIST]->(m)
        """)

    with driver.session() as session:
        # Create or Match User
        session.run(user_query)

        # Create Watchlist Relationships
        for query in watchlist_queries:
            session.run(query)

    print("User and their watchlist have been added to the Neo4j database.")


def neo4j_add_relation_actor_movie_director(driver):
    # Queries for Movies, Actors, Directors, and Relationships
    movie_queries = [
        "CREATE (:Movie {id: 1, title: 'Inception', release_year: 2010, rating: 8.8, genre: 'Sci-Fi', duration: 148})",
        "CREATE (:Movie {id: 2, title: 'Interstellar', release_year: 2014, rating: 8.6, genre: 'Sci-Fi', duration: 169})"
    ]

    actor_queries = [
        "CREATE (:Actor {description: 'Main actor in Inception', type: 'ACTOR', name: 'Leonardo DiCaprio', movie_id: 1})",
        "CREATE (:Actor {description: 'Main actor in Interstellar', type: 'ACTOR', name: 'Matthew McConaughey', movie_id: 2})",
        "CREATE (:Actor {description: 'Supporting actor in Interstellar', type: 'ACTOR', name: 'Anne Hathaway', movie_id: 2})"
    ]

    director_queries = [
        "CREATE (:Director {description: 'Director of Inception', type: 'DIRECTOR', name: 'Christopher Nolan', movie_id: 1})",
        "CREATE (:Director {description: 'Director of Interstellar', type: 'DIRECTOR', name: 'Christopher Nolan', movie_id: 2})"
    ]

    relationship_queries = [
        "MATCH (d:Director {movie_id: 1}), (m:Movie {id: 1}) CREATE (d)-[:DIRECTED]->(m)",
        "MATCH (d:Director {movie_id: 2}), (m:Movie {id: 2}) CREATE (d)-[:DIRECTED]->(m)",
        "MATCH (a:Actor {movie_id: 1}), (m:Movie {id: 1}) CREATE (a)-[:ACTED_IN]->(m)",
        "MATCH (a:Actor {movie_id: 2}), (m:Movie {id: 2}) CREATE (a)-[:ACTED_IN]->(m)"
    ]

    # Execute Queries
    with driver.session() as session:
        for query in movie_queries:
            session.run(query)

        for query in actor_queries:
            session.run(query)

        for query in director_queries:
            session.run(query)

        for query in relationship_queries:
            session.run(query)

    print("All data and relationships have been added to the Neo4j database.")

def check_all_data(driver):
    query = """
    MATCH (n)
    RETURN labels(n) AS Labels, n AS Properties
    """
    with driver.session() as session:
        result = session.run(query)
        for record in result:
            print(f"Labels: {record['Labels']}, Properties: {record['Properties']}")
            print()


def clear_database(driver):
    """
    Deletes all nodes and relationships from the Neo4j database.

    Args:
        driver (neo4j.Driver): The Neo4j driver object.
    """
    query = "MATCH (n) DETACH DELETE n"
    with driver.session() as session:
        session.run(query)
    print("All data has been deleted from the Neo4j database.")

def neo4j_close_sess(driver)->bool: #DONE
    driver.close()


def check_data_in_db(driver):
    with driver.session() as session:
        # Check movies
        print("\nMovies in the database:")
        movies = session.run("""
            MATCH (m:Movie)
            RETURN m.id AS ID, m.title AS Title, m.release_year AS ReleaseYear, 
                   m.rating AS Rating, m.genre AS Genre, m.duration AS Duration
        """)
        for record in movies:
            print(record)

        # Check actors
        print("\nActors in the database:")
        actors = session.run("""
            MATCH (a:Actor)
            RETURN a.name AS Name, a.description AS Description, 
                   a.type AS Type, a.movie_id AS MovieID
        """)
        for record in actors:
            print(record)

        # Check directors
        print("\nDirectors in the database:")
        directors = session.run("""
            MATCH (d:Director)
            RETURN d.name AS Name, d.description AS Description, 
                   d.type AS Type, d.movie_id AS MovieID
        """)
        for record in directors:
            print(record)

        # Check relationships
        print("\nDirectors and their Movies:")
        directed = session.run("""
            MATCH (d:Director)-[:DIRECTED]->(m:Movie)
            RETURN d.name AS Director, m.title AS Movie
        """)
        for record in directed:
            print(record)

        print("\nActors and their Movies:")
        acted_in = session.run("""
            MATCH (a:Actor)-[:ACTED_IN]->(m:Movie)
            RETURN a.name AS Actor, m.title AS Movie
        """)
        for record in acted_in:
            print(record)


def find_watchlist_for_user(driver, user_id):
    query = """
    MATCH (u:User {user_id: $user_id})-[:WATCHLIST]->(m:Movie)
    RETURN u.name AS User, m.title AS Movie, m.release_year AS ReleaseYear
    """
    with driver.session() as session:
        result = session.run(query, user_id=user_id)
        for record in result:
            print(f"User: {record['User']}, Movie: {record['Movie']}, Release Year: {record['ReleaseYear']}")


def find_users_for_movie(driver, movie_id):
    query = """
    MATCH (u:User)-[:WATCHLIST]->(m:Movie {id: $movie_id})
    RETURN m.title AS Movie, u.name AS User, u.email AS Email
    """
    with driver.session() as session:
        result = session.run(query, movie_id=movie_id)
        for record in result:
            print(f"Movie: {record['Movie']}, User: {record['User']}, Email: {record['Email']}")


def get_all_reviews(driver):
    """
    Retrieves all reviews with user and movie details.
    
    Args:
        driver (neo4j.Driver): The Neo4j driver object.
    """
    query = """
    MATCH (u:User)-[:REVIEWS]->(r:Review)-[:REVIEWS]->(m:Movie)
    RETURN 
        u.user_id AS ReviewerID,
        r.review_id AS ReviewID,
        r.rating AS Rating,
        m.title AS MovieTitle,
        m.release_year AS ReleaseYear
    ORDER BY Rating DESC
    """
    with driver.session() as session:
        result = session.run(query)
        for record in result:
            print(f"Reviewer: {record['ReviewerID']}, "
                  f"ReviewID: {record['ReviewID']}, Rating: {record['Rating']}, "
                  f"MovieTitle: {record['MovieTitle']}, ReleaseYear: {record['ReleaseYear']}")



