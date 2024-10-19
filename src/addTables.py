import sqlite3

database = sqlite3.connect('db_project_1.db')
cursor = database.cursor()

# User
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL
)
''')

# Subscription
cursor.execute('''
CREATE TABLE IF NOT EXISTS subscriptions (
    id INTEGER PRIMARY KEY,
    subscription_type TEXT NOT NULL,
    start_date DATE,
    end_date DATE,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')


# Reviews 
cursor.execute('''
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY,
    rating FLOAT,
    comment TEXT,
    movie_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY(movie_id) REFERENCES movies(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')


# Directors
cursor.execute('''
CREATE TABLE IF NOT EXISTS directors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
''')

# Watchlist
cursor.execute('''
CREATE TABLE IF NOT EXISTS watchlists (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    movie_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(movie_id) REFERENCES movies(id)
)
''')

# Actors
cursor.execute('''
CREATE TABLE IF NOT EXISTS actors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
''')


database.commit()
database.close()
