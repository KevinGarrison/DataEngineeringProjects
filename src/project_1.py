from utils import setup

from datetime import date

from sqlalchemy import inspect

from new_classes import (
    SubscriptionType,
    CastType,
)
from new_classes import (
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
from sqlalchemy import MetaData, inspect

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

def populate_users(session):
    """Populates the User and MainUser tables with sample data."""
    main_user = MainUser(
        username="john_doe",
        email="john@example.com",
        iban="DE89370400440532013000",
        price=29.99,
        subscription_type=SubscriptionType.MONTHLY,
        start_date=date(2023, 1, 1),
        end_date=date(2024, 1, 1)
    )
    
    other_user = OtherUser(
        username="jane_doe",
        email="jane@example.com"
    )

    session.add(main_user)
    session.add(other_user)
    session.commit()

def print_users(session):
    """Prints all entries in the User, MainUser, and OtherUser tables."""
    users = session.query(User).all()
    for user in users:
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Type: {user.user_type}")


def populate_watchlists(session):
    """Populates the Watchlist table with sample data."""
    main_user = session.query(MainUser).first()
    
    watchlist = Watchlist(user=main_user)
    session.add(watchlist)
    session.commit()

def print_watchlists(session):
    """Prints all entries in the Watchlist table."""
    watchlists = session.query(Watchlist).all()
    for watchlist in watchlists:
        print(f"ID: {watchlist.id}, User ID: {watchlist.user_id}")

def populate_media(session):
    """Populates the Media, Movie, and Series tables with sample data."""
    movie = Movie(
        title="Inception",
        release_year=2010,
        rating=8.8,
        genre="Sci-Fi",
        duration=148
    )

    series = Series(
        title="Breaking Bad",
        release_year=2008,
        rating=9.5,
        genre="Crime",
        season_count=5
    )

    session.add(movie)
    session.add(series)
    session.commit()

def print_media(session):
    """Prints all entries in the Media, Movie, and Series tables."""
    media_items = session.query(Media).all()
    for media in media_items:
        if isinstance(media, Movie):
            print(
                f"Movie ID: {media.id}, Title: {media.title}, Release Year: {media.release_year}, "
                f"Rating: {media.rating}, Genre: {media.genre}, Duration: {media.duration}"
            )
        elif isinstance(media, Series):
            print(
                f"Series ID: {media.id}, Title: {media.title}, Release Year: {media.release_year}, "
                f"Rating: {media.rating}, Genre: {media.genre}, Seasons: {media.season_count}"
            )
        else:
            print(
                f"Media ID: {media.id}, Title: {media.title}, Release Year: {media.release_year}, "
                f"Rating: {media.rating}, Genre: {media.genre}"
            )

def populate_cast(session):
    """Populates the Cast, Director, and Actor tables with sample data."""
    movie = session.query(Movie).first()
    series = session.query(Series).first()
    
    director = Director(
        description="Director of Inception",
        type=CastType.DIRECTOR,
        name="Christopher Nolan",
        movie=movie
    )

    actor = Actor(
        description="Main actor in Breaking Bad",
        type=CastType.ACTOR,
        name="Bryan Cranston",
        series=series
    )

    session.add(director)
    session.add(actor)
    session.commit()


def print_cast(session):
    """Prints all entries in the Cast, Director, and Actor tables."""
    cast_items = session.query(Cast).all()
    for cast in cast_items:
        if isinstance(cast, Director):
            print(f"Director ID: {cast.id}, Name: {cast.name}, Description: {cast.description}")
        elif isinstance(cast, Actor):
            print(f"Actor ID: {cast.id}, Name: {cast.name}, Description: {cast.description}")
        else:
            print(f"Cast ID: {cast.id}, Description: {cast.description}, Type: {cast.type}")


def populate_episodes(session):
    """Populates the Episode table with sample data."""
    series = session.query(Series).first()

    episode1 = Episode(
        title="Pilot",
        episode_number=1,
        series=series
    )
    
    episode2 = Episode(
        title="Cat's in the Bag...",
        episode_number=2,
        series=series
    )

    session.add(episode1)
    session.add(episode2)
    session.commit()


def print_episodes(session):
    """Prints all entries in the Episode table."""
    episodes = session.query(Episode).all()
    for episode in episodes:
        print(
            f"Episode ID: {episode.id}, Title: {episode.title}, Episode Number: {episode.episode_number}, "
            f"Series ID: {episode.series_id}"
        )


def populate_reviews(session):
    """Populates the Review table with sample data."""
    user = session.query(User).first()
    media = session.query(Media).first()

    review = Review(
        rating=9.0,
        user=user,
        media=media
    )

    session.add(review)
    session.commit()


def print_reviews(session):
    """Prints all entries in the Review table."""
    reviews = session.query(Review).all()
    for review in reviews:
        print(
            f"Review ID: {review.id}, Rating: {review.rating}, User ID: {review.user_id}, Media ID: {review.media_id}"
        )


def populate_watchlist_media(session):
    """Populates the watchlist-media many-to-many relationship with sample data."""
    watchlist = session.query(Watchlist).first()
    media = session.query(Media).all()

    watchlist.media.extend(media)  # Add all media to the watchlist
    session.commit()


def print_watchlist_media(session):
    """Prints the media items associated with each watchlist."""
    watchlists = session.query(Watchlist).all()
    for watchlist in watchlists:
        print(f"Watchlist ID: {watchlist.id} (User ID: {watchlist.user_id}) has media items:")
        for media in watchlist.media:
            print(f"  - Media ID: {media.id}, Title: {media.title}")


from sqlalchemy import func

def count_media_per_user(session):
    """Counts the number of media items in each user's watchlist."""
    result = session.query(
        User.username,
        func.count(Media.id).label('media_count')
    ).join(Watchlist, User.id == Watchlist.user_id) \
     .join(watchlist_media, Watchlist.id == watchlist_media.c.watchlists_id) \
     .join(Media, Media.id == watchlist_media.c.medias_id) \
     .group_by(User.id) \
     .all()

    for username, media_count in result:
        print(f"Username: {username}, Media Count: {media_count}")

def average_rating_by_genre(session):
    """Calculates the average rating of movies and series by genre."""
    result = session.query(
        Media.genre,
        func.avg(Media.rating).label('average_rating')
    ).group_by(Media.genre) \
     .all()

    for genre, avg_rating in result:
        print(f"Genre: {genre}, Average Rating: {avg_rating:.2f}")


def count_reviews_per_media(session):
    """Counts the number of reviews per media item."""
    result = session.query(
        Media.title,
        func.count(Review.id).label('review_count')
    ).join(Review, Media.id == Review.media_id) \
     .group_by(Media.id) \
     .all()

    for title, review_count in result:
        print(f"Media Title: {title}, Review Count: {review_count}")

def total_revenue_by_subscription_type(session):
    """Calculates total revenue by subscription type."""
    result = session.query(
        Subscription.subscription_type,
        func.sum(Subscription.price).label('total_revenue')
    ).group_by(Subscription.subscription_type) \
     .all()

    for sub_type, total_revenue in result:
        print(f"Subscription Type: {sub_type}, Total Revenue: ${total_revenue:.2f}")

def count_episodes_per_series(session):
    """Counts the number of episodes per series."""
    result = session.query(
        Series.title,
        func.count(Episode.id).label('episode_count')
    ).join(Episode, Series.id == Episode.series_id) \
     .group_by(Series.id) \
     .all()

    for title, episode_count in result:
        print(f"Series Title: {title}, Episode Count: {episode_count}")

if __name__ == "__main__":
    database = 'database.db'

    try:
        session, engine = setup(database)
        
        #result = drop_all_tables(engine)
        #print(result)
        #inspector = inspect(engine)
        #tables = inspector.get_table_names()

        #for table in tables:
         #   print(table)
        
        #populate_users(session=session)
        #print_users(session=session)

        #populate_watchlists(session=session)

        #print_watchlists(session=session)

        #populate_media(session=session)

        #print_media(session=session)

        #populate_cast(session=session)

        #print_cast(session=session)

        #populate_episodes(session=session)

        #print_episodes(session=session)

        #populate_reviews(session=session)

        #print_reviews(session=session)

        #populate_watchlist_media(session=session)

        #print_watchlist_media(session=session)
        
        count_media_per_user(session)
        average_rating_by_genre(session)
        count_reviews_per_media(session)
        total_revenue_by_subscription_type(session)
        count_episodes_per_series(session)


    except Exception as e:
        print(f"An error occurred: {e}")


