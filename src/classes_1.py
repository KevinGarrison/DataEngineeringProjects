from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum


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
    review_id = Column(Integer, ForeignKey('reviews.id'))
    watchlist_id = Column(Integer, ForeignKey('watchlists.id'))

    # Many-to-One relationship with Account
    watchlists = relationship('User', back_populates='watchlists', uselist=False)
    reviews = relationship('User', back_populates='reviews')

    # Polymorphic identity
    __mapper_args__ = {
        'polymorphic_identity': 'users',
        'polymorphic_on': user_type,
    }


class MainUser(User):
    __tablename__ = 'main_users'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True, autoincrement=True)
    subscription_id = Column(Integer, ForeignKey('subscriptions.id'))

    subscriptions = relationship('MainUser', back_populates='subscriptions', cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': UserType.MAIN_USER,
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

    main_users = relationship('Subscription', back_populates='main_users')


class OtherUser(User):
    __tablename__ = 'other_users'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True, autoincrement=True)

    __mapper_args__ = {
        'polymorphic_identity': UserType.OTHER_USER,
    }


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, autoincrement=True)
    rating = Column(Float)

    # Foreign Keys
    user_id = Column(Integer, ForeignKey('users.id'))
    media_id = Column(Integer, ForeignKey('medias.id'))

    # Many-to-One relationships
    users = relationship('Review', back_populates='users')
    medias = relationship('Review', back_populates='medias')


class Watchlist(Base):
    __tablename__ = 'watchlists'
    id = Column(Integer, primary_key=True, autoincrement=True)
    media_id = Column(Integer, ForeignKey('medias.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    users = relationship('Watchlist', back_populates='users', uselist=False)
    medias = relationship('Watchlist', back_populates='medias')


class Media(Base):
    __tablename__ = 'medias'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    release_year = Column(Integer, nullable=False)
    rating = Column(Float)
    genre = Column(String(200), nullable=False)
    media_type = Column(Enum(MediaType), nullable=False)

    watchlist_id = Column(Integer, ForeignKey('watchlists.id'))
    review_id = Column(Integer, ForeignKey('reviews.id'))

    watchlists = relationship('Media', back_populates='watchlists')
    reviews = relationship('Media', back_populates='reviews', uselist=False)

    # Polymorphic identity
    __mapper_args__ = {
        'polymorphic_identity': 'medias',
        'polymorphic_on': media_type,
    }


class Movie(Media):
    __tablename__ = 'movies'
    id = Column(Integer, ForeignKey('medias.id'), primary_key=True, autoincrement=True)
    duration = Column(Integer, nullable=False)

    cast_id = Column(Integer, ForeignKey('casts.id'))

    casts = relationship('Movie', back_populates='casts')

    __mapper_args__ = {
        'polymorphic_identity': MediaType.MOVIE
    }


class Series(Media):
    __tablename__ = 'series'
    id = Column(Integer, ForeignKey('medias.id'), primary_key=True, autoincrement=True)
    season_count = Column(Integer, nullable=False)
    episode_id = Column(Integer, ForeignKey('episodes.id'))
    cast_id = Column(Integer, ForeignKey('casts.id'))

    # One-to-Many relationship with Episodes
    episodes = relationship('Series', back_populates='episodes', cascade="all, delete-orphan")
    casts = relationship('Cast', back_populates='series')

    __mapper_args__ = {
        'polymorphic_identity': MediaType.SERIES
    }


class Cast(Base):
    __tablename__ = 'casts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(200), nullable=False)
    type = Column(Enum(CastType), nullable=False)

    # Foreign Keys
    movie_id = Column(Integer, ForeignKey('movies.id'))
    series_id = Column(Integer, ForeignKey('series.id'))

    # Relationships
    movies = relationship('Cast', back_populates='movies')
    series = relationship('Cast', back_populates='series')

    __mapper_args__ = {
        'polymorphic_identity': 'casts',
        'polymorphic_on': type,
    }


class Episode(Base):
    __tablename__ = 'episodes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    episode_number = Column(Integer, nullable=False)

    # Foreign Key
    series_id = Column(Integer, ForeignKey('series.id'))

    # Relationship back to Series
    series = relationship('Episode', back_populates='series')


class Director(Cast):
    __tablename__ = 'directors'
    id = Column(Integer, ForeignKey('casts.id'), primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': CastType.DIRECTOR,
    }


class Actor(Cast):
    __tablename__ = 'actors'
    id = Column(Integer, ForeignKey('casts.id'), primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': CastType.ACTOR,
    }

