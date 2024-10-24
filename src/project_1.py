import sqlite3
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utils import setup

database = 'database.db'

try:
    session = setup(database)
    

except sqlite3.Error as e:
    session.rollback()
    print(f"An error occurred: {e}")
finally:
    if session:
        .close()
    if connection:
        connection.close()

   
