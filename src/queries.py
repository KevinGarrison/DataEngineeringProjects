from sqlalchemy import func
from classes import (
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

    def count_media_per_user(self, session):
        """Counts the number of media items in each user's watchlist."""
        result = session.query(
            User.username,
            func.count(Media.id).label('media_count')
        ).join(Watchlist, User.id == Watchlist.user_id) \
        .join(watchlist_media, Watchlist.id == watchlist_media.c.watchlists_id) \
        .join(Media, Media.id == watchlist_media.c.medias_id) \
        .group_by(User.id) \
        .all()

        r = []
        for username, media_count in result:
            r.append([username, media_count])
            print(f"Username: {username}, Media Count: {media_count}")
        return r
    

    def average_rating_by_genre(self, session):
        """Calculates the average rating of movies and series by genre."""
        result = session.query(
            Media.genre,
            func.avg(Media.rating).label('average_rating')
        ).group_by(Media.genre) \
        .all()
        r = []
        for genre, avg_rating in result:
            r.append([genre, avg_rating])
            print(f"Genre: {genre}, Average Rating: {avg_rating:.2f}")
        return r

    def count_reviews_per_media(self, session):
        """Counts the number of reviews per media item."""
        result = session.query(
            Media.title,
            func.count(Review.id).label('review_count')
        ).join(Review, Media.id == Review.media_id) \
        .group_by(Media.id) \
        .all()
        r = []
        for title, review_count in result:
            r.append([title, review_count])
            print(f"Media Title: {title}, Review Count: {review_count}")
        return r
    
    
    def total_revenue_by_subscription_type(self, session):
        """Calculates total revenue by subscription type."""
        result = session.query(
            Subscription.subscription_type,
            func.sum(Subscription.price).label('total_revenue')
        ).group_by(Subscription.subscription_type) \
        .all()

        for sub_type, total_revenue in result:
            print(f"Subscription Type: {sub_type}, Total Revenue: ${total_revenue:.2f}")

    def count_episodes_per_series(self, session):
        """Counts the number of episodes per series."""
        result = session.query(
            Series.title,
            func.count(Episode.id).label('episode_count')
        ).join(Episode, Series.id == Episode.series_id) \
        .group_by(Series.id) \
        .all()

        r = []
        for title, episode_count in result:
            r.append([title, episode_count])
            print(f"Series Title: {title}, Episode Count: {episode_count}")
        return r