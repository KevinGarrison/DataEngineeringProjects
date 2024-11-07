from datetime import date
import json
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


def populate_watchlists(session):
    """Populates the Watchlist table with sample data."""
    main_user = session.query(MainUser).first()
    
    watchlist = Watchlist(user=main_user)
    session.add(watchlist)
    session.commit()


def populate_media(session):
    """Populates the Media, Movie, and Series tables with sample data."""
    movie = Movie(
        id = 1,
        title="Inception",
        release_year=2010,
        rating=8.8,
        genre="Sci-Fi",
        duration=148
    )

    series = Series(
        id = 2,
        title="Breaking Bad",
        release_year=2008,
        rating=9.5,
        genre="Crime",
        season_count=5
    )

    session.add(movie)
    session.add(series)
    session.commit()


def populate_cast(session):
    """Populates the Cast, Director, and Actor tables with sample data."""
    movie = session.query(Movie).filter_by(id=1).first()
    series = session.query(Series).filter_by(id=2).first()
    
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


def populate_watchlist_media(session):
    """Populates the watchlist-media many-to-many relationship with sample data."""
    watchlist = session.query(Watchlist).first()
    media = session.query(Media).all()

    watchlist.media.extend(media)  
    session.commit()


def create_single_cast(session, filename):
    with open(filename) as jsonfile:
        cast_data = json.load(jsonfile)
        #movie = session.query(Movie).filter_by(id=2).first()
        #series = session.query(Series).filter_by(id=1).first()
        
        director_data = cast_data["director"]
        director = Director(
            series_id=1,
            description=director_data["description"],
            type=CastType.DIRECTOR,
            name=director_data["name"],
            #series=series
        )
        actor_data = cast_data["actor"]
        actor = Actor(
            movie_id=1,
            description=actor_data["description"],
            type=CastType.ACTOR,
            name=actor_data["name"],
            #series=series
        )
        
        

        session.add(director)
        session.add(actor)
        session.commit()
        
