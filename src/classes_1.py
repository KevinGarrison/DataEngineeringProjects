from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
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

# Account Class
class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # One-to-One relationship with Watchlist
    watchlist_id = Column(Integer, ForeignKey('watchlists.id'))
    watchlist = relationship("Watchlist", back_populates="account", uselist=False)
    
    # One-to-Many relationships
    users = relationship("User", back_populates="account")
    payments = relationship("Payment", back_populates="account")
    reviews = relationship("Review", back_populates="account")

# User Class
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    user_type = Column(Enum(UserType), nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'))

    # Many-to-One relationship with Account
    account = relationship('Account', back_populates='users')

    # Polymorphic identity
    __mapper_args__ = {
        'polymorphic_identity': 'users',
        'polymorphic_on': user_type,
    }

class MainUser(User):
    __tablename__ = 'main_users'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': UserType.MAIN_USER,
    }

class OtherUser(User):
    __tablename__ = 'other_users'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': UserType.OTHER_USER,
    }

# Payment Class
class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    iban = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    subscription_type = Column(Enum(SubscriptionType), nullable=False)

    # Foreign Key
    account_id = Column(Integer, ForeignKey('accounts.id'))

    # Many-to-One relationship with Account
    account = relationship('Account', back_populates='payments')

# Review Class
class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, autoincrement=True)
    rating = Column(Float)
    comment = Column(String(300))

    # Foreign Keys
    account_id = Column(Integer, ForeignKey('accounts.id'))
    media_id = Column(Integer, ForeignKey('medias.id'))

    # Many-to-One relationships
    account = relationship('Account', back_populates='reviews')
    media = relationship('Media', back_populates='reviews')

# Watchlist Class
class Watchlist(Base):
    __tablename__ = 'watchlists'
    id = Column(Integer, primary_key=True, autoincrement=True)

    # One-to-One relationship with Account
    account = relationship('Account', back_populates='watchlist', uselist=False)

    # One-to-Many relationship with Media
    media = relationship('Media', back_populates='watchlist', cascade="all, delete-orphan")

# Media Class
class Media(Base):
    __tablename__ = 'medias'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    release_year = Column(Integer, nullable=False)
    rating = Column(Float)
    genre = Column(String(200), nullable=False)
    media_type = Column(Enum(MediaType), nullable=False)

    # Foreign Key
    watchlist_id = Column(Integer, ForeignKey('watchlists.id'))

    # Many-to-One relationship with Watchlist
    watchlist = relationship('Watchlist', back_populates='media')

    # One-to-Many relationship with Review
    reviews = relationship('Review', back_populates='media')

    # Polymorphic identity
    __mapper_args__ = {
        'polymorphic_identity': 'medias',
        'polymorphic_on': media_type,
    }

class Movie(Media):
    __tablename__ = 'movies'
    id = Column(Integer, ForeignKey('medias.id'), primary_key=True)
    duration = Column(Integer, nullable=False)  # Changed to Integer

    # Foreign Key for configuration and cast
    configuration_id = Column(Integer, ForeignKey('configurations.id'))

    # Relationships
    configuration = relationship('Configuration', back_populates='movie', foreign_keys=[configuration_id])
    cast = relationship('Cast', back_populates='movie', cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': MediaType.MOVIE
    }

class Series(Media):
    __tablename__ = 'series'
    id = Column(Integer, ForeignKey('medias.id'), primary_key=True)
    season_count = Column(Integer, nullable=False)

    # One-to-Many relationship with Episodes
    episodes = relationship('Episode', back_populates='series')

    # Foreign Key for configuration and cast
    configuration_id = Column(Integer, ForeignKey('configurations.id'))

    # Relationships
    configuration = relationship('Configuration', back_populates='series', foreign_keys=[configuration_id])
    cast = relationship('Cast', back_populates='series', cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': MediaType.SERIES
    }

# Configuration Class
class Configuration(Base):
    __tablename__ = 'configurations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    language = Column(String, nullable=False)
    subtitles = Column(Boolean, nullable=False)
    quality = Column(Integer, nullable=False)

    # Relationships
    movie = relationship('Movie', back_populates='configuration', foreign_keys='Movie.configuration_id')
    series = relationship('Series', back_populates='configuration', foreign_keys='Series.configuration_id')

# Cast Class
class Cast(Base):
    __tablename__ = 'casts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(200), nullable=False)
    type = Column(Enum(CastType), nullable=False)

    # Foreign Keys
    movie_id = Column(Integer, ForeignKey('movies.id'))
    series_id = Column(Integer, ForeignKey('series.id'))

    # Relationships
    movie = relationship('Movie', back_populates='cast')
    series = relationship('Series', back_populates='cast')

    __mapper_args__ = {
        'polymorphic_identity': 'casts',
        'polymorphic_on': type,
    }

# Episode Class
class Episode(Base):
    __tablename__ = 'episodes'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    episode_number = Column(Integer, nullable=False)

    # Foreign Key
    series_id = Column(Integer, ForeignKey('series.id'))

    # Relationship back to Series
    series = relationship('Series', back_populates='episodes')

# Director Class
class Director(Cast):
    __tablename__ = 'directors'
    id = Column(Integer, ForeignKey('casts.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': CastType.DIRECTOR,
    }

# Actor Class
class Actor(Cast):
    __tablename__ = 'actors'
    id = Column(Integer, ForeignKey('casts.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': CastType.ACTOR,
    }
