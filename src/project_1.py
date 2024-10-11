import sqlite3

try:
    con = sqlite3.connect('db_project_1.db')
    cur = con.cursor()
except sqlite3.Error as e:
    print(f"An error occurred: {e}")
finally:
    if con:
        con.close()
