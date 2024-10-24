from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Enum
from enum import Enum as PyEnum


Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    payment_id = Column(Integer, ForeignKey('payments.id'))

    user = relationship('User', back_populates='account')
    payments = relationship('Payment', back_populates='account', cascade="all, delete-orphan")


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


# MainUser class
class MainUser(User):
    __tablename__ = 'main_users'
    
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': UserType.MAIN_USER  # Specify the identity for this subclass
    }

    # Additional attributes specific to MainUser
    additional_attribute = Column(String)


# OtherUser class
class OtherUser(User):
    __tablename__ = 'other_users'
    
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': UserType.OTHER_USER  # Specify the identity for this subclass
    }



class Subscription(Base):
    __tablename__ = 'subscriptions'
    
    id = Column(Integer, primary_key=True)
    subscription_type = Column(String(20), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    # Relationship (assuming a relationship with a User class)
    user = relationship('User', back_populates='subscriptions')
    def __repr__(self):
        return f"<Subscription(type={self.subscription_type}, start={self.start_date}, end={self.end_date}, user={self.user_id})>"


class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True)
    rating = Column(Float)
    comment = Column(String(300))
    media_id = Column(Integer, ForeignKey('movies.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    
    # Relationships
    media = relationship('Media', back_populates='reviews')
    user = relationship('User', back_populates='reviews')

    def __repr__(self):
        return f"<Rating(rating={self.rating}, comment={self.comment}, movie={self.media.title}, user={self.user.username})>"
    

class Cast(Base):
    __tablename__ = 'cast'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'cast'
    }


class Director(Cast):
    __tablename__ = 'directors'
    
    id = Column(Integer, ForeignKey('cast.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'director'  # Identity for Director subclass
    }
    
    # Relationship to movies (directed by a Director)
    media = relationship('Media', back_populates='director')

    def __repr__(self):
        return f"<Director(name={self.name})>"


class Actor(Base):
    __tablename__ = 'actors'
    
    id = Column(Integer, ForeignKey('cast.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'actor'  # Identity for Director subclass
    }
    
    # Relationship to movies (directed by a Director)
    media = relationship('Media', back_populates='actor')

    def __repr__(self):
        return f"<Actor(name={self.name})>"


class Media(Base):
    __tablename__ = 'media'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_year = Column(Integer)
    rating = Column(Float)
    genre = Column(String(200))
    
    # Relationships
    cast = relationship('Cast', back_populates='media')
    reviews = relationship('Review', back_populates='media')
    # Column to determine the type of media (movie or series)
    media_type = Column(String(50))
    
    __mapper_args__ = {
        'polymorphic_on': media_type,  # Use media_type to distinguish between subclasses
        'polymorphic_identity': 'media'  # Default identity for the base class
    }

# Subclass for Movie (no additional attributes needed)
class Movie(Media):

    __mapper_args__ = {
        'polymorphic_identity': 'movie'  # Set the polymorphic identity to 'movie'
    }

# Subclass for Series (with additional attributes for Series)
class Series(Media):
    __tablename__ = 'series'
    
    id = Column(Integer, ForeignKey('media.id'), primary_key=True)
    season_count = Column(Integer)  # Additional attribute specific to series
    episodes = relationship('Episode', back_populates='series', cascade="all, delete-orphan")
    
    __mapper_args__ = {
        'polymorphic_identity': 'series'
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


class Watchlist(Base):
    __tablename__ = 'watchlists'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))
    
    # Relationships
    user = relationship('User', back_populates='watchlists')
    movie = relationship('Movie', back_populates='watchlists')

    def __repr__(self):
        return f"<Watchlist(user={self.user.username}, movie={self.movie.title})>"
