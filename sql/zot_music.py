from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Table, Date, Text, CheckConstraint, \
    TIMESTAMP, text, Index, and_, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from constants import MySQLDBUrl, DBName

Base = declarative_base()

# Users Table
class User(Base):
    __tablename__ = 'Users'  # Plural table name

    user_id = Column(String(255), primary_key=True)
    email = Column(String(255), nullable=False)
    joined_date = Column(Date, nullable=False)
    nickname = Column(String(255), nullable=False)
    street = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    zip = Column(String(10))
    genres = Column(String(255))

# Artists Table
class Artist(Base):
    __tablename__ = 'Artists'  # Plural table name

    user_id = Column(String(255), ForeignKey('Users.user_id', ondelete='CASCADE'), primary_key=True)
    stagename = Column(String(255))
    bio = Column(Text)

    user = relationship('User')

# Listeners Table
class Listener(Base):
    __tablename__ = 'Listeners'  # Plural table name

    user_id = Column(String(255), ForeignKey('Users.user_id', ondelete='CASCADE'), primary_key=True)
    subscription = Column(String(50), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)

    user = relationship('User')

# Records Table
class Record(Base):
    __tablename__ = 'Records'  # Plural table name

    record_id = Column(String(255), primary_key=True)
    artist_user_id = Column(String(255), ForeignKey('Artists.user_id', ondelete='CASCADE'))
    title = Column(String(255), nullable=False)
    genre = Column(String(30), nullable=False)  # Changed to match schema
    release_date = Column(Date, nullable=False)

    artist = relationship('Artist')

# Singles Table
class Single(Base):
    __tablename__ = 'Singles'  # Plural table name

    record_id = Column(String(255), ForeignKey('Records.record_id', ondelete='CASCADE'), primary_key=True)
    video_url = Column(Text)

    record = relationship('Record')

# Albums Table
class Album(Base):
    __tablename__ = 'Albums'  # Plural table name

    record_id = Column(String(255), ForeignKey('Records.record_id', ondelete='CASCADE'), primary_key=True)
    description = Column(Text)

    record = relationship('Record')

# Songs Table
class Song(Base):
    __tablename__ = 'Songs'  # Plural table name

    record_id = Column(String(255), ForeignKey('Records.record_id', ondelete='CASCADE'), primary_key=True)
    track_number = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    length = Column(Integer, nullable=False)  # Song length in seconds
    bpm = Column(Integer)
    mood = Column(String(255))

    record = relationship('Record')

    # Composite index for the foreign key relation with Session
    __table_args__ = (
        Index('ix_song_record_track', 'record_id', 'track_number'),
    )

# Sessions Table
class Session(Base):
    __tablename__ = 'Sessions'  # Plural table name

    session_id = Column(String(255), primary_key=True)
    user_id = Column(String(255), ForeignKey('Listeners.user_id', ondelete='CASCADE'))
    record_id = Column(String(255), nullable=False)
    track_number = Column(Integer, nullable=False)
    initiate_at = Column(TIMESTAMP, nullable=False)
    leave_at = Column(TIMESTAMP, nullable=False)
    music_quality = Column(String(255), nullable=False)
    device = Column(String(255), nullable=False)
    end_play_time = Column(Integer, nullable=False)  # how long this session is
    replay_count = Column(Integer)

    listener = relationship('Listener')

    # Composite foreign key relationship with the Song table
    song = relationship(
        'Song',
        foreign_keys=[record_id, track_number],
        primaryjoin=and_(
            record_id == Song.record_id,
            track_number == Song.track_number
        )
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ['record_id', 'track_number'],
            ['Songs.record_id', 'Songs.track_number'],
            ondelete="CASCADE"
        ),
    )

# Reviews Table
class Review(Base):
    __tablename__ = 'Reviews'  # Plural table name

    review_id = Column(String(255), primary_key=True)
    user_id = Column(String(255), ForeignKey('Listeners.user_id', ondelete='CASCADE'))
    record_id = Column(String(255), ForeignKey('Records.record_id', ondelete='CASCADE'))
    rating = Column(Integer, nullable=False)
    body = Column(Text)
    posted_at = Column(TIMESTAMP, nullable=False)

    listener = relationship('Listener')
    record = relationship('Record')

# ReviewLikes Table
class ReviewLike(Base):
    __tablename__ = 'ReviewLikes'  # Plural table name

    user_id = Column(String(255), ForeignKey('Listeners.user_id', ondelete='CASCADE'), primary_key=True)
    review_id = Column(String(255), ForeignKey('Reviews.review_id', ondelete='CASCADE'), primary_key=True)

    listener = relationship('Listener')
    review = relationship('Review')


def drop_and_create_db(mysql_url, db_name):
    """
    Drop the specified database and recreate it.
    :param mysql_url: The MySQL connection URL without the database name (e.g., 'mysql+pymysql://user:password@localhost')
    :param db_name: The name of the database to drop and recreate
    """
    # Connect to MySQL without specifying the database
    engine = create_engine(mysql_url)

    # Drop the database if it exists, then recreate it
    with engine.connect() as connection:
        connection.execute(text(f"DROP DATABASE IF EXISTS {db_name};"))
        connection.execute(text(f"CREATE DATABASE {db_name};"))

    # Update the engine to connect to the newly created database
    engine = create_engine(f"{mysql_url}/{db_name}")

    # Create all tables
    Base.metadata.create_all(engine)

    # Set up the session
    Session = sessionmaker(bind=engine)
    session = Session()

    return session


session = drop_and_create_db(MySQLDBUrl, DBName)
