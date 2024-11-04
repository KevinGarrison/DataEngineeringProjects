from sqlalchemy import func
from src.classes import (
    User,
    Media,
    Watchlist,
    Review,
    Subscription,
    Episode,
    Series,
    watchlist_media
)


class Queries:

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