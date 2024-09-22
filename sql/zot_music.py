from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Table, Date, Text, CheckConstraint, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

# Association tables for many-to-many relationships
UserGenres = Table(
    'user_genres', Base.metadata,
    Column('user_id', String(255), ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.genre_id', ondelete='CASCADE'), primary_key=True)
)

RecordGenres = Table(
    'record_genres', Base.metadata,
    Column('record_id', String(255), ForeignKey('records.record_id', ondelete='CASCADE'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.genre_id', ondelete='CASCADE'), primary_key=True)
)

# Genres Table
class Genre(Base):
    __tablename__ = 'genres'

    genre_id = Column(Integer, primary_key=True)
    genre_name = Column(String(255), nullable=False)

# Users Table
class User(Base):
    __tablename__ = 'users'

    user_id = Column(String(255), primary_key=True)
    email = Column(String(255), nullable=False)
    joined_date = Column(Date, nullable=False)
    nickname = Column(String(255), nullable=False)
    street = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    zip = Column(String(10))

    # Many-to-many relationship with genres
    genres = relationship('Genre', secondary=UserGenres, backref='users')

# Artists Table
class Artist(Base):
    __tablename__ = 'artists'

    user_id = Column(String(255), ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    bio = Column(Text)

    user = relationship('User')

# Listeners Table
class Listener(Base):
    __tablename__ = 'listeners'

    user_id = Column(String(255), ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    subscription = Column(String(50), CheckConstraint("subscription IN ('free', 'monthly', 'yearly')"))
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)

    user = relationship('User')

# Records Table
class Record(Base):
    __tablename__ = 'records'

    record_id = Column(String(255), primary_key=True)
    artist_user_id = Column(String(255), ForeignKey('artists.user_id', ondelete='CASCADE'))
    title = Column(String(255), nullable=False)
    release_date = Column(Date)

    artist = relationship('Artist')
    genres = relationship('Genre', secondary=RecordGenres, backref='records')

# Singles Table
class Single(Base):
    __tablename__ = 'singles'

    record_id = Column(String(255), ForeignKey('records.record_id', ondelete='CASCADE'), primary_key=True)
    video_url = Column(Text, nullable=False)

    record = relationship('Record')

# Albums Table
class Album(Base):
    __tablename__ = 'albums'

    record_id = Column(String(255), ForeignKey('records.record_id', ondelete='CASCADE'), primary_key=True)
    description = Column(Text)

    record = relationship('Record')

# Songs Table
class Song(Base):
    __tablename__ = 'songs'

    record_id = Column(String(255), ForeignKey('records.record_id', ondelete='CASCADE'), primary_key=True)
    track_number = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    length = Column(Integer, nullable=False)  # Song length in seconds
    bpm = Column(Integer)
    mood = Column(String(255), nullable=False)

    record = relationship('Record')

# Sessions Table
class Session(Base):
    __tablename__ = 'sessions'

    session_id = Column(String(255), primary_key=True)
    user_id = Column(String(255), ForeignKey('listeners.user_id', ondelete='CASCADE'))
    record_id = Column(String(255), ForeignKey('songs.record_id', ondelete='CASCADE'))
    track_number = Column(Integer, ForeignKey('songs.track_number', ondelete='CASCADE'))
    initiate_at = Column(TIMESTAMP, nullable=False)
    leave_at = Column(TIMESTAMP, nullable=False)
    music_quality = Column(String(255), nullable=False)
    device = Column(String(255), nullable=False)
    start_timestamp = Column(TIMESTAMP, nullable=False)  # Start timestamp for song play
    end_timestamp = Column(TIMESTAMP, nullable=False)    # End timestamp for song play
    replay_count = Column(Integer)

    listener = relationship('Listener')
    song = relationship(
        'Song',
        foreign_keys=[record_id, track_number],  # Explicitly define foreign keys here
        primaryjoin='and_(Session.record_id == Song.record_id, Session.track_number == Song.track_number)'
    )


# Reviews Table
class Review(Base):
    __tablename__ = 'reviews'

    review_id = Column(String(255), primary_key=True)
    user_id = Column(String(255), ForeignKey('listeners.user_id', ondelete='CASCADE'))
    record_id = Column(String(255), ForeignKey('records.record_id', ondelete='CASCADE'))
    rating = Column(Integer, nullable=False)
    body = Column(Text)
    posted_at = Column(TIMESTAMP, nullable=False)

    listener = relationship('Listener')
    record = relationship('Record')

# ReviewLikes Table
class ReviewLike(Base):
    __tablename__ = 'review_likes'

    user_id = Column(String(255), ForeignKey('listeners.user_id', ondelete='CASCADE'), primary_key=True)
    review_id = Column(String(255), ForeignKey('reviews.review_id', ondelete='CASCADE'), primary_key=True)

    listener = relationship('Listener')
    review = relationship('Review')

# Set up the engine and create the tables
engine = create_engine('mysql+pymysql://root:123456@localhost/ZotMusicMysql')  # Update with your MySQL connection details
# Base.metadata.create_all(engine)

# Set up the session
Session = sessionmaker(bind=engine)
session = Session()
