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
import json


def print_users(session):
    """Prints all entries in the User, MainUser, and OtherUser tables."""
    users = session.query(User).all()
    for user in users:
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Type: {user.user_type}")


def print_watchlists(session):
    """Prints all entries in the Watchlist table."""
    watchlists = session.query(Watchlist).all()
    for watchlist in watchlists:
        print(f"ID: {watchlist.id}, User ID: {watchlist.user_id}")


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


def print_episodes(session):
    """Prints all entries in the Episode table."""
    episodes = session.query(Episode).all()
    for episode in episodes:
        print(
            f"Episode ID: {episode.id}, Title: {episode.title}, Episode Number: {episode.episode_number}, "
            f"Series ID: {episode.series_id}"
        )


def print_reviews(session):
    """Prints all entries in the Review table."""
    reviews = session.query(Review).all()
    for review in reviews:
        print(
            f"Review ID: {review.id}, Rating: {review.rating}, User ID: {review.user_id}, Media ID: {review.media_id}"
        )


def print_watchlist_media(session):
    """Prints the media items associated with each watchlist."""
    watchlists = session.query(Watchlist).all()
    for watchlist in watchlists:
        print(f"Watchlist ID: {watchlist.id} (User ID: {watchlist.user_id}) has media items:")
        for media in watchlist.media:
            print(f"  - Media ID: {media.id}, Title: {media.title}")


def to_dict(instance):
    return {key: value for key, value in instance.__dict__.items() if not key.startswith('_')}


def reviewandwatchlist_to_json(session):
    review = session.query(Review).filter_by(id=1).first()
    watchlist = session.query(Watchlist).filter_by(id=1).first()
    
    review = to_dict(review)
    watchlist = to_dict(watchlist)
    with open("src/reviewwatchlist.json", "w") as json_file:
        json.dump(review, json_file, indent=4)
        json.dump(watchlist, json_file, indent=4)
