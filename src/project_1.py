from utils import setup, add_content

if __name__ == "__main__":
    database = 'database.db'

    try:
        # Setup the database and get session
        session, engine = setup(database)
        
        # Add an account associated with the user
        add_content(session=session, condition="accounts", user_id=1, balance=1000.50)

        if session:
            session.close()
        if engine:
            engine.dispose()

        
    except Exception as e:
        print(f"An error occurred: {e}")


