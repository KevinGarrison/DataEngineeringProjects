import sqlite3
from sqlalchemy import create_engine

try:
    con = sqlite3.connect('db_project_1.db')
    cur = con.cursor()
    engine = create_engine('sqlite:///db_project_1.db')
    connection = engine.connect()
except sqlite3.Error as e:
    print(f"An error occurred: {e}")
finally:
    if con:
        con.close()
    if connection:
        connection.close()
