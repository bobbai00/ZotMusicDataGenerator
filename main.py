import csv
import os

from constants import TargetFormat
from exports.csv_exporter import export_csvs
from generators.viewer_review_release import create_reviews
from generators.viewer_session_video import create_sessions_gaussian
from generators.release_movie_series_video import create_releases_movies_series_videos
from generators.user_producer_viewer import create_users_producers_viewers
from sql.zot_streaming import session

if __name__ == "__main__":
    # Create users, viewers, and producers and insert them into the database
    users, viewers, producers = create_users_producers_viewers()

    # Commit users, viewers, and producers first
    session.add_all(users + producers + viewers)
    session.commit()
    print("Finished inserting users, viewers, and producers.")

    # Create releases, movies, series, and videos
    releases, movies, series_list, videos = create_releases_movies_series_videos(producers)

    # Commit releases, movies, series, and videos
    session.add_all(releases + movies + series_list + videos)
    session.commit()
    print("Finished inserting releases, movies, series, and videos.")

    # Create sessions and commit them
    sessions = create_sessions_gaussian(viewers, videos)
    session.add_all(sessions)
    session.commit()
    print("Finished inserting sessions.")

    # Create reviews and commit them
    reviews = create_reviews(viewers, releases)
    session.add_all(reviews)
    session.commit()
    print("Finished inserting reviews.")

    print(f"Created {len(users)} users, {len(viewers)} viewers, {len(producers)} producers, {len(releases)} releases, "
          f"{len(movies)} movies, {len(series_list)} series, {len(videos)} videos, {len(sessions)} sessions, "
          f"{len(reviews)} reviews.")