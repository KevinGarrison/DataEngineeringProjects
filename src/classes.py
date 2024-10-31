from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Date, Table
from sqlalchemy.orm import relationship, declarative_base
from enum import Enum as PyEnum

# Enums for Subscription, User Type, Media Type, and Cast Type
class SubscriptionType(PyEnum):
    MONTHLY = "Monthly"
    YEARLY = "Yearly"
    TEST = "Test"

class UserType(PyEnum):
    MAIN_USER = "Main User"
    OTHER_USER = "Other User"

class MediaType(PyEnum):
    MOVIE = 'Movie'
    SERIES = 'Series'

class CastType(PyEnum):
    ACTOR = 'Actor'
    DIRECTOR = 'Director'

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    user_type = Column(Enum(UserType), nullable=False)

    # Relationships
    watchlist = relationship('Watchlist', back_populates='user', uselist=False)
    reviews = relationship('Review', back_populates='user')

    # Polymorphic identity
    __mapper_args__ = {
        'polymorphic_identity': 'users',
        'polymorphic_on': user_type,
    }

class MainUser(User):
    __tablename__ = 'main_users'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    subscriptions = relationship('Subscription', back_populates='main_user', cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': UserType.MAIN_USER,
    }

class OtherUser(User):
    __tablename__ = 'other_users'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': UserType.OTHER_USER,
    }

class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    iban = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    subscription_type = Column(Enum(SubscriptionType), nullable=False)
    startdate = Column(Date, nullable=False)
    enddate = Column(Date, nullable=False)
    main_user_id = Column(Integer, ForeignKey('main_users.id'))

    main_user = relationship('MainUser', back_populates='subscriptions')

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, autoincrement=True)
    rating = Column(Float)

    user_id = Column(Integer, ForeignKey('users.id'))
    media_id = Column(Integer, ForeignKey('medias.id'))

    user = relationship('User', back_populates='reviews')
    media = relationship('Media', back_populates='reviews')

class Watchlist(Base):
    __tablename__ = 'watchlists'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='watchlist')
    medias = relationship('Media', secondary='watchlist_media', back_populates='watchlists')

class WatchlistMedia(Base):
    __tablename__ = 'watchlist_media'
    watchlist_id = Column(Integer, ForeignKey('watchlists.id'), primary_key=True)
    media_id = Column(Integer, ForeignKey('medias.id'), primary_key=True)

class Media(Base):
    __tablename__ = 'medias'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    release_year = Column(Integer, nullable=False)
    rating = Column(Float)
    genre = Column(String(200), nullable=False)
    media_type = Column(Enum(MediaType), nullable=False)

    watchlists = relationship('Watchlist', secondary='watchlist_media', back_populates='medias')
    reviews = relationship('Review', back_populates='media')

    __mapper_args__ = {
        'polymorphic_identity': 'medias',
        'polymorphic_on': media_type,
    }

class Movie(Media):
    __tablename__ = 'movies'
    id = Column(Integer, ForeignKey('medias.id'), primary_key=True)
    duration = Column(Integer, nullable=False)

    cast_id = Column(Integer, ForeignKey('casts.id'))

    casts = relationship('Cast', back_populates='movies', uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': MediaType.MOVIE
    }

class Series(Media):
    __tablename__ = 'series'
    id = Column(Integer, ForeignKey('medias.id'), primary_key=True)
    season_count = Column(Integer, nullable=False)
    cast_id = Column(Integer, ForeignKey('casts.id'))  # ForeignKey added

    episodes = relationship('Episode', back_populates='series', cascade="all, delete-orphan")
    casts = relationship('Cast', primaryjoin="Series.cast_id == Cast.id", uselist=False)  # primaryjoin added

    __mapper_args__ = {
        'polymorphic_identity': MediaType.SERIES
    }

class Cast(Base):
    __tablename__ = 'casts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(200), nullable=False)
    type = Column(Enum(CastType), nullable=False)

    movies = relationship('Movie', back_populates='casts', uselist=False)
    series = relationship('Series', back_populates='casts', uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': 'casts',
        'polymorphic_on': type,
    }

class Episode(Base):
    __tablename__ = 'episodes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    episode_number = Column(Integer, nullable=False)
    series_id = Column(Integer, ForeignKey('series.id'))

    series = relationship('Series', back_populates='episodes')

class Director(Cast):
    __tablename__ = 'directors'
    id = Column(Integer, ForeignKey('casts.id'), primary_key=True)
    name = Column(String(200), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': CastType.DIRECTOR,
    }

class Actor(Cast):
    __tablename__ = 'actors'
    id = Column(Integer, ForeignKey('casts.id'), primary_key=True)
    name = Column(String(200), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': CastType.ACTOR,
    }
