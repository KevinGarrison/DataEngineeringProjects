from utils import setup, add_content


if __name__ == "__main__":
    database = 'database.db'

    try:
        Session, engine = setup(database)
        
        session = Session()
        while(1):
            add_content(session, "Action")
    
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if session:
            session.close()
        if engine:
            engine.dispose()