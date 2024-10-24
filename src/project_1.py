from utils import setup, add_content
from classes_1 import (
    #Base,
    Account,
    Payment,
    User,
    MainUser,
    OtherUser,
    #Subscription,
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


if __name__ == "__main__":
    database = 'database.db'

    try:
        # Setup the database and get session
        session, engine = setup(database)

        add_content(session=session, condition='main_users', username="MainUser1", email="main@example.com", account_id=1)
        add_content(session, 'other_users', username='janedoe', email='jane@example.com',account_id=2)

        users = session.query(MainUser).all()

        for user in users:
            print(user.username, user.email)
        if session:
            session.close()
        if engine:
            engine.dispose()

        
    except Exception as e:
        print(f"An error occurred: {e}")


