from utils import setup, drop_all_tables
import populate_data as ppd
import print_data as prd
from queries import Queries
from sqlalchemy import inspect



from classes import (
    SubscriptionType,
    CastType,
)


from classes import (
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
        
        result = drop_all_tables(engine)
        print(result)
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        session, engine = setup(database)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print("Create tables:")
        for table in tables:
           print(table)
        print("These database is filled with:")
        ppd.populate_users(session)
        prd.print_users(session)

        ppd.populate_watchlists(session)
        prd.print_watchlists(session)

        

        ppd.populate_media(session)
        prd.print_media(session)

        ppd.populate_reviews(session)
        prd.print_reviews(session)

        ppd.populate_watchlist_media(session)
        prd.print_watchlist_media(session)

        ppd.create_single_cast(session, "src\cast.json")
        prd.print_cast(session)
        prd.print_media(session)

        ppd.create_other_user(session,"src\otheruser.json")
        prd.print_users(session)


        # add description of class in to_dict
        prd.reviewandwatchlist_to_json(session)

        # ppd.populate_cast(session)
        # prd.print_cast(session)

        # ppd.populate_episodes(session)
        # prd.print_episodes(session)
        
        # ppd.populate_reviews(session)
        # prd.print_reviews(session)

        # ppd.populate_watchlist_media(session)
        # prd.print_watchlist_media(session)

        # print("Here start the queries: ")
        
        # print("      Count the media per user ")
        # queries.count_media_per_user(session)
        # print("      Calculate the average rating by genre ")
        # queries.average_rating_by_genre(session)
        # print("      Count the reviews per media ")
        # queries.count_reviews_per_media(session)
        # print("      Calculate the revenue by subscription ")
        # queries.total_revenue_by_subscription_type(session)
        # print("      Count the episodes per season ")
        # queries.count_episodes_per_series(session)

        if session:
            session.close()
        if engine:
            engine.dispose()

    except Exception as e:
        print(f"An error occurred: {e}")


