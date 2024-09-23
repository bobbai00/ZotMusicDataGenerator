import csv
import os

from constants import TargetFormat
from exports.csv import export_csvs
from generators.listener_like_review import create_review_likes
from generators.listener_review_record import create_reviews
from generators.listener_session_song import create_sessions
from generators.record_single_album_song import create_records_singles_albums_songs
from generators.user_artist_listener import create_users_listeners_artists
from sql.zot_music import session

if __name__ == "__main__":
    # Create genres, users, listeners, and artists and insert them into the database
    users, listeners, artists = create_users_listeners_artists()

    # Commit genres, users, listeners, and artists first
    session.add_all(users + artists + listeners)
    session.commit()

    # Create records, singles, albums, and songs
    records, singles, albums, songs = create_records_singles_albums_songs(artists)

    # Commit records, singles, albums, and songs
    session.add_all(records + singles + albums + songs)
    session.commit()

    # Create sessions and commit them
    sessions = create_sessions(listeners, songs)
    session.add_all(sessions)
    session.commit()

    # Create reviews and commit them
    reviews = create_reviews(listeners, records)
    session.add_all(reviews)
    session.commit()

    # Create review likes and commit them
    review_likes = create_review_likes(reviews, listeners)
    session.add_all(review_likes)
    session.commit()

    print(f"Created {len(users)} users, {len(listeners)} listeners, {len(artists)} artists, {len(records)} records, "
          f"{len(singles)} singles, {len(albums)} albums, {len(songs)} songs, {len(sessions)} sessions, "
          f"{len(reviews)} reviews, {len(review_likes)} review likes.")

    # Export CSVs if the target format is CSV
    if TargetFormat == "csv":
        export_csvs(users, listeners, artists, records, singles, albums, songs, sessions, reviews, review_likes)