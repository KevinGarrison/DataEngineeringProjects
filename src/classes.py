from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, REAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from enum import Enum as PyEnum


Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    payment_id = Column(Integer, ForeignKey('payments.id'))

    user = relationship('User', back_populates='account')
    payments = relationship('Payment', back_populates='account', cascade="all, delete-orphan")
    reviews = relationship('Review', back_populates='account', cascade="all, delete-orphan")


class SubscriptionType(PyEnum):
    MONTHLY = "Monthly"
    YEARLY = "Yearly"
    TEST = "Test"


class Payment(Base):
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True)
    iban = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    subscription_type = Column(Enum(SubscriptionType), nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'))

    # Relationship back to Account
    account = relationship('Account', back_populates='payments')

    def __repr__(self):
        return f"<Payment(amount={self.amount}, method={self.payment_method})>"


class UserType(PyEnum):
    MAIN_USER = "Main User"
    OTHER_USER = "Other User"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    user_type = Column(Enum(UserType), nullable=False)

    account = relationship('Account', back_populates='user', uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': user_type  # This will determine which subclass to use
    }

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"


class MainUser(User):
    __tablename__ = 'main_users'
    
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': UserType.MAIN_USER  # Specify the identity for this subclass
    }

    # Additional attributes specific to MainUser
    additional_attribute = Column(String)


class OtherUser(User):
    __tablename__ = 'other_users'
    
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': UserType.OTHER_USER  # Specify the identity for this subclass
    }


class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True)
    rating = Column(Float)
    comment = Column(String(300))
    media_id = Column(Integer, ForeignKey('movies.id'))
    account_id = Column(Integer, ForeignKey('accounts.id'))

    media = relationship('Media', back_populates='reviews')
    account = relationship('Account', back_populates='reviews')

    def __repr__(self):
        return f"<Rating(rating={self.rating}, comment={self.comment}, movie={self.media.title}, user={self.account.user.username})>"


class Watchlist(Base):
    __tablename__ = 'watchlists'
    
    id = Column(Integer, primary_key=True)
    #user_id = Column(Integer, ForeignKey('users.id'))
    account_id = Column(Integer, ForeignKey('accounts.id'))
    media_id = Column(Integer, ForeignKey('movies.id'))
    
    #user = relationship('User', back_populates='watchlists')
    account = relationship('Account', back_populates='watchlists')
    media = relationship('Media', back_populates='watchlists')

    def __repr__(self):
        return f"<Watchlist(user={self.account.user.username}, movie={self.media.movie.title})>"


class Cast(Base):
    __tablename__ = 'casts'
    
    id = Column(Integer, primary_key=True)
    description = Column(String)
    media_id = Column(Integer, ForeignKey('media.id'))  # Foreign key to Media
    actor_names = Column(String, nullable=False)  # Actor's name as a simple attribute
    director_name = Column(String, nullable=False)  # Director's name as a simple attribute

    # Relationships
    media = relationship('Media', back_populates='cast')


class MediaType(Enum):
    MOVIE = "Movie"
    SERIES = "Series"


class Media(Base):
    __tablename__ = 'media'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_year = Column(Integer)
    rating = Column(Float)
    genre = Column(String(200))
    media_type = Column(Enum(MediaType), nullable=False)
    
    # Relationships
    cast = relationship('Cast', back_populates='media')
    reviews = relationship()
    
    __mapper_args__ = {
        'polymorphic_on': media_type,  # Use media_type to distinguish between subclasses
        'polymorphic_identity': 'media'  # Default identity for the base class
    }

# Subclass for Movie (no additional attributes needed)
class Movie(Media):

    __mapper_args__ = {
        'polymorphic_identity': MediaType.MOVIE  # Set the polymorphic identity to 'movie'
    }

# Subclass for Series (with additional attributes for Series)
class Series(Media):
    __tablename__ = 'series'
    
    id = Column(Integer, ForeignKey('media.id'), primary_key=True)
    season_count = Column(Integer)  # Additional attribute specific to series
    episodes = relationship('Episode', back_populates='series', cascade="all, delete-orphan")
    
    __mapper_args__ = {
        'polymorphic_identity': MediaType.SERIES
    }

# Episodes of a Series
class Episode(Base):
    __tablename__ = 'episodes'
    
    episode_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    episode_number = Column(Integer, nullable=False)
    series_id = Column(Integer, ForeignKey('series.id'))  # Link to the Series
    
    # Relationship back to the series
    series = relationship('Series', back_populates='episodes')

    def __repr__(self):
        return f"<Episode(title={self.title}, episode_number={self.episode_number})>"


