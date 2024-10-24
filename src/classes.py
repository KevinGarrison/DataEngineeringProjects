from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, REAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable = False)

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
    

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

    __mapper_args__ = {
        'polymorphic_on': 'type',
        'polymorphic_identity': 'cast'
    }


class Director(Cast):
    __tablename__ = 'directors'
    
    id = Column(Integer, ForeignKey('cast.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'director'  # Identity for Director subclass
    }
    
    # Relationship to movies (directed by a Director)
    meida = relationship('Media', back_populates='director')

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
    # Liste 
    genre = Column()
    director_id = Column(Integer, ForeignKey('directors.id'))
    actor_id = Column(Integer, ForeignKey('actors.id'))
    
    # Relationships
    director = relationship('Director', back_populates='movies')
    reviews = relationship('Review', back_populates='movie')
    watchlists = relationship('Watchlist', back_populates='movie')
    series = relationship('Series', back_populates='movie')
    
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
    
    __mapper_args__ = {
        'polymorphic_identity': 'series'  # Set the polymorphic identity to 'series'
    }


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



    

class Movie(Base):
    __tablename__ = 'movies'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_year = Column(Integer)
    rating = Column(REAL)
    genre_id = Column(Integer, ForeignKey('genres.id'))
    director_id = Column(Integer, ForeignKey('directors.id'))
    
    # Relationships
    director = relationship('Director', back_populates='movies')
    reviews = relationship('Review', back_populates='movie')
    watchlists = relationship('Watchlist', back_populates='movie')
    series = relationship('Series', back_populates='movie')
    
    def __repr__(self):
        return f"<Movie(title={self.title}, genre={self.genre}, director={self.director}, rating={self.rating})>"


class Movie(Base):
    __tablename__ = 'movies'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    genre = Column(String(50), nullable=False)
    director = Column(String(100))
    release_date = Column(Date)
    rating = Column(Float)
    
    def __repr__(self):
        return f"<Movie(title={self.title}, genre={self.genre}, director={self.director}, rating={self.rating})>"