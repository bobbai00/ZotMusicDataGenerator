from sqlalchemy import (
    create_engine, Column, String, Integer, ForeignKey, Table, Date, Text, Enum, TIMESTAMP, Index, and_,
    ForeignKeyConstraint
)
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import text
from constants import MySQLDBUrl, DBName

Base = declarative_base()

# Users Table
class User(Base):
    __tablename__ = 'Users'

    uid = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(Text, nullable=False)
    joined_date = Column(Date, nullable=False)
    nickname = Column(Text, nullable=False)
    street = Column(Text)
    city = Column(Text)
    state = Column(Text)
    zip = Column(String(10))
    genres = Column(Text)

    producers = relationship("Producer", back_populates="user", cascade="all, delete-orphan")
    viewers = relationship("Viewer", back_populates="user", cascade="all, delete-orphan")


# Producers Table (ISA Relationship)
class Producer(Base):
    __tablename__ = 'Producers'

    uid = Column(Integer, ForeignKey('Users.uid', ondelete="CASCADE"), primary_key=True)
    bio = Column(Text)
    company = Column(Text)

    user = relationship("User", back_populates="producers")
    releases = relationship("Release", back_populates="producer")


# Viewers Table (ISA Relationship)
class Viewer(Base):
    __tablename__ = 'Viewers'

    uid = Column(Integer, ForeignKey('Users.uid', ondelete="CASCADE"), primary_key=True)
    subscription = Column(Enum('free', 'monthly', 'yearly'), nullable=False)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)

    user = relationship("User", back_populates="viewers")
    sessions = relationship("Session", back_populates="viewer")
    reviews = relationship("Review", back_populates="viewer")


# Releases Table
class Release(Base):
    __tablename__ = 'Releases'

    rid = Column(Integer, primary_key=True, autoincrement=True)
    producer_uid = Column(Integer, ForeignKey('Producers.uid', ondelete="CASCADE"), nullable=False)
    title = Column(Text, nullable=False)
    genre = Column(Text, nullable=False)
    release_date = Column(Date, nullable=False)

    producer = relationship("Producer", back_populates="releases")
    movies = relationship("Movie", back_populates="release", cascade="all, delete-orphan")
    series = relationship("Series", back_populates="release", cascade="all, delete-orphan")
    videos = relationship("Video", back_populates="release", cascade="all, delete-orphan")


# Movies Table (ISA Relationship)
class Movie(Base):
    __tablename__ = 'Movies'

    rid = Column(Integer, ForeignKey('Releases.rid', ondelete="CASCADE"), primary_key=True)
    website_url = Column(Text)

    release = relationship("Release", back_populates="movies")


# Series Table (ISA Relationship)
class Series(Base):
    __tablename__ = 'Series'

    rid = Column(Integer, ForeignKey('Releases.rid', ondelete="CASCADE"), primary_key=True)
    introduction = Column(Text)

    release = relationship("Release", back_populates="series")


# Videos Table (Weak Entity)
class Video(Base):
    __tablename__ = 'Videos'

    rid = Column(Integer, ForeignKey('Releases.rid', ondelete="CASCADE"), primary_key=True)
    ep_num = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    length = Column(Integer, nullable=False)  # In seconds

    release = relationship("Release", back_populates="videos")


# Sessions Table
class Session(Base):
    __tablename__ = 'Sessions'

    sid = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer, ForeignKey('Viewers.uid', ondelete="CASCADE"), nullable=False)
    rid = Column(Integer, nullable=False)
    ep_num = Column(Integer, nullable=False)
    initiate_at = Column(TIMESTAMP, nullable=False)
    leave_at = Column(TIMESTAMP, nullable=False)
    quality = Column(Enum('480p', '720p', '1080p'))
    device = Column(Enum('mobile', 'desktop'))

    viewer = relationship("Viewer", back_populates="sessions")

    # Composite Foreign Key
    __table_args__ = (
        ForeignKeyConstraint(['rid', 'ep_num'], ['Videos.rid', 'Videos.ep_num'], ondelete="CASCADE"),
    )


# Reviews Table
class Review(Base):
    __tablename__ = 'Reviews'

    rvid = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer, ForeignKey('Viewers.uid', ondelete="CASCADE"), nullable=False)
    rid = Column(Integer, ForeignKey('Releases.rid', ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)
    body = Column(Text)
    posted_at = Column(TIMESTAMP, nullable=False)

    viewer = relationship("Viewer", back_populates="reviews")
    release = relationship("Release")


# Database Creation Utilities
def create_db_if_not_exists(mysql_url, db_name):
    """
    Check if the database exists, create it if it doesn't.
    """
    engine = create_engine(mysql_url)
    with engine.connect() as connection:
        try:
            connection.execute(text(f"USE {db_name};"))
            print(f"Database {db_name} exists. No need to create it.")
        except OperationalError:
            print(f"Database {db_name} does not exist. Creating it.")
            connection.execute(text(f"CREATE DATABASE {db_name};"))


def drop_and_create_tables(mysql_url, db_name):
    """
    Drop all tables in the database (if they exist) and recreate them.
    """
    create_db_if_not_exists(mysql_url, db_name)

    engine = create_engine(f"{mysql_url}/{db_name}")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    print(f"All tables in the database '{db_name}' have been dropped and recreated.")
    return session


# Usage
session = drop_and_create_tables(MySQLDBUrl, DBName)