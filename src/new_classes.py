from __future__ import annotations

from sqlalchemy import CheckConstraint
from typing import List, Optional
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from datetime import date

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

class Base(DeclarativeBase):
    pass

# Core Table watchlist_media many to many

watchlist_media = Table(
    "watchlist_media",
    Base.metadata,
    Column("medias_id", ForeignKey("medias.id"), primary_key=True),
    Column("watchlists_id", ForeignKey("watchlists.id"), primary_key=True),
)


class User(Base):
    __tablename__ = 'users'

    # Attributes
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    user_type: Mapped[UserType] = mapped_column(nullable=False)

    # Relationships
    watchlist: Mapped["Watchlist"] = relationship(back_populates='user')
    review: Mapped[Optional[List["Review"]]] = relationship(back_populates='user')

    # Polymorphic identity
    __mapper_args__ = {
        'polymorphic_identity': 'users',
        'polymorphic_on': user_type,
    }


class MainUser(User):
    __tablename__ = 'main_users'
    
    # Attributes
    id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)

    # Relationships
    subscription: Mapped["Subscription"] = relationship(back_populates='main_user', cascade="all, delete-orphan", uselist=False)

    # Constructor for Subscription composition
    def __init__(self, username, email, iban, price, subscription_type, start_date, end_date):
        self.username = username
        self.email = email
        self.user_type = UserType.MAIN_USER
        # Create a subscription instance associated with this MainUser
        self.subscription = Subscription(
            iban=iban,
            price=price,
            subscription_type=subscription_type,
            startdate=start_date,
            enddate=end_date,
        )

    # Polymorphic identity
    __mapper_args__ = {
        'polymorphic_identity': UserType.MAIN_USER,
    }


class OtherUser(User):
    __tablename__ = 'other_users'

    # Attributes
    id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)

    # Polymorphic identity
    __mapper_args__ = {
        'polymorphic_identity': UserType.OTHER_USER,
    }


class Subscription(Base):
    __tablename__ = 'subscriptions'

    # Attributes
    id: Mapped[int] = mapped_column(primary_key=True)
    iban: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    subscription_type: Mapped[SubscriptionType] = mapped_column(nullable=False)
    startdate: Mapped[date] = mapped_column(nullable=False)
    enddate: Mapped[date] = mapped_column(nullable=False)
    main_user_id: Mapped[int] = mapped_column(ForeignKey('main_users.id'), nullable=False)

    # Relationships
    main_user: Mapped["MainUser"] = relationship(back_populates='subscription')


class Watchlist(Base):
    __tablename__ = 'watchlists'
    
    # Attributes
    id:Mapped[int] = mapped_column(primary_key=True,)
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))
    
    # Relationships
    user:Mapped["User"] = relationship(back_populates='watchlist', single_parent=True)
    media:Mapped[List["Media"]] = relationship(secondary='watchlist_media', back_populates='watchlist') 


class Media(Base):
    __tablename__ = 'medias'

    # Attributes
    id:Mapped[int] = mapped_column(primary_key=True,)
    title:Mapped[str] = mapped_column(nullable=False)
    release_year:Mapped[int] = mapped_column(nullable=False)
    rating:Mapped[float] = mapped_column()
    genre:Mapped[str] = mapped_column(nullable=False)
    media_type:Mapped[MediaType] = mapped_column(nullable=False)

    # Relationships
    watchlist:Mapped[Optional[List["Watchlist"]]] = relationship(secondary='watchlist_media', back_populates='media') 
    review:Mapped[Optional[List["Review"]]] = relationship(back_populates='media')

    # Polymorphic identity
    __mapper_args__ = {
        'polymorphic_identity': 'medias',
        'polymorphic_on': media_type,
    }

    
class Review(Base):
    __tablename__ = 'reviews'

    # Attributes
    id:Mapped[int] = mapped_column(primary_key=True,)
    rating:Mapped[float] = mapped_column()
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))
    media_id:Mapped[int] = mapped_column(ForeignKey('medias.id'))

    # Relationships
    user:Mapped["User"] = relationship(back_populates='review')
    media:Mapped["Media"] = relationship(back_populates='review')


class Cast(Base):
    __tablename__ = 'casts'

    # Attributes
    id:Mapped[int] = mapped_column(primary_key=True,)
    description:Mapped[str] = mapped_column(nullable=False)
    type:Mapped[CastType] = mapped_column(nullable=False)
    movie_id:Mapped[int] = mapped_column(ForeignKey('movies.id'), nullable=True)
    series_id:Mapped[int] = mapped_column(ForeignKey('series.id'), nullable=True)

    # Relationships
    movie:Mapped["Movie"] = relationship(back_populates='cast',)
    series:Mapped["Series"] = relationship(back_populates='cast',)

    # Polymorphic identity
    __mapper_args__ = {
        'polymorphic_identity': 'casts',
        'polymorphic_on': type,
    }

    # Check constraint
    __table_args__ = (
        CheckConstraint(
            '(movie_id IS NOT NULL AND series_id IS NULL) OR (movie_id IS NULL AND series_id IS NOT NULL)',
            name='only_one_foreign_key'
        ),
    )


class Movie(Media):
    __tablename__ = 'movies'

    # Attributes
    id:Mapped[int] = mapped_column(ForeignKey('medias.id'), primary_key=True)
    duration:Mapped[int] = mapped_column(nullable=False)

    # Relationships
    cast:Mapped[List["Cast"]] = relationship(back_populates='movie')

    # Polymorphic identity
    __mapper_args__ = {
        'polymorphic_identity': MediaType.MOVIE
    }


class Series(Media):
    __tablename__ = 'series'

    # Attributes
    id:Mapped[int] = mapped_column(ForeignKey('medias.id'), primary_key=True)
    season_count:Mapped[int] = mapped_column(nullable=False)

    # Relationships
    episode:Mapped[List["Episode"]] = relationship(back_populates='series', cascade="all, delete-orphan")
    cast:Mapped[List["Cast"]] = relationship(back_populates='series')

    # Polymorphic identity
    __mapper_args__ = {
        'polymorphic_identity': MediaType.SERIES
    }


class Episode(Base):
    __tablename__ = 'episodes'

    # Attributes
    id:Mapped[int] = mapped_column(primary_key=True,)
    title:Mapped[str] = mapped_column(nullable=False)
    episode_number:Mapped[int] = mapped_column(nullable=False)
    series_id:Mapped[int] = mapped_column(ForeignKey('series.id'), nullable=False)

    # Relationships
    series:Mapped["Series"] = relationship(back_populates='episode')


class Director(Cast):
    __tablename__ = 'directors'

    # Attributes
    id:Mapped[int] = mapped_column(ForeignKey('casts.id'), primary_key=True)
    name:Mapped[str] = mapped_column(nullable=False)

    # Polymorphic identity
    __mapper_args__ = {
        'polymorphic_identity': CastType.DIRECTOR,
    }


class Actor(Cast):
    __tablename__ = 'actors'

    # Attributes
    id:Mapped[int] = mapped_column(ForeignKey('casts.id'), primary_key=True)
    name:Mapped[str] = mapped_column(nullable=False)

    # Polymorphic identity
    __mapper_args__ = {
        'polymorphic_identity': CastType.ACTOR,
    }
