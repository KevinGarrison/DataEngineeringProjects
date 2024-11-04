from utils import setup, drop_all_tables
from populate_data import populate_data
from queries import Queries


from src.classes import (
    SubscriptionType,
    CastType,
)
from src.classes import (
    User,
    MainUser,
    Subscription,
    OtherUser,
    Review,
    Cast,
    Director,
    Actor,
    Media,
    Movie,
    Series,
    Episode,
    Watchlist,
    watchlist_media
)

if __name__ == "__main__":
    database = 'database.db'

    try:
        session, engine = setup(database)

        queries = Queries()
        
        #result = drop_all_tables(engine)
        #print(result)
        #inspector = inspect(engine)
        #tables = inspector.get_table_names()

        #for table in tables:
         #   print(table)
        
        populate_data(session)
        
        queries.count_media_per_user(session)
        queries.average_rating_by_genre(session)
        queries.count_reviews_per_media(session)
        queries.total_revenue_by_subscription_type(session)
        queries.count_episodes_per_series(session)


    except Exception as e:
        print(f"An error occurred: {e}")


