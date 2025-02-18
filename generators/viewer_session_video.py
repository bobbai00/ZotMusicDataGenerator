from typing import List
import random
from faker import Faker
from datetime import datetime, timedelta

from generators.release_movie_series_video import create_releases_movies_series_videos
from generators.user_producer_viewer import create_users_producers_viewers
from sql.zot_streaming import Video, Session, Viewer, session
from constants import (
    NumberOfSessions, EarliestSessionStartTime, Seed, VIDEO_QUALITY_OPTIONS, DEVICE_OPTIONS, NullValueProbability
)

# Initialize Faker with seed
faker = Faker()
random.seed(Seed)
Faker.seed(Seed)

# Function to randomly return None with a certain probability
def random_null(probability=0.2):
    return None if random.random() < probability else True

# Function to generate a random number of sessions for each viewer using a Gaussian distribution
def generate_gaussian_sessions(mean=100, std_dev=50, max_sessions=200):
    num_sessions = abs(random.gauss(mean, std_dev))
    return int(min(max_sessions, num_sessions))  # Clamp to max_sessions

# Function to select a video using Gaussian distribution
def select_video_gaussian(videos: List[Video], mean=0, std_dev=10):
    index = int(random.gauss(mean, std_dev))
    index = max(0, min(len(videos) - 1, index))  # Clamp index within valid range
    return videos[index]

# Function to create sessions using Gaussian distribution with scaled parameters
def create_sessions_gaussian(viewers: List[Viewer], videos: List[Video]) -> List[Session]:
    sessions = []

    for viewer in viewers:
        # Generate the number of sessions for this viewer with a higher mean and standard deviation
        num_sessions = generate_gaussian_sessions(mean=200, std_dev=150, max_sessions=400)

        for _ in range(num_sessions):
            sid = len(sessions) + 1  # Sequential session ID

            # Select a video using Gaussian distribution
            video = select_video_gaussian(videos, mean=len(videos) / 2, std_dev=len(videos) / 4)

            # Ensure session length does not exceed video length
            session_length = random.randint(1, video.length)

            # Generate random start time
            start_time = faker.date_time_between(start_date=EarliestSessionStartTime, end_date="now")

            # Calculate the end time based on the session length
            end_time = start_time + timedelta(seconds=session_length)

            # Add a random delta (pause) to the end_time
            pause_delta = timedelta(seconds=random.randint(0, 100))
            end_time_with_delta = end_time + pause_delta

            # Create the session object
            session_obj = Session(
                sid=sid,
                uid=viewer.uid,
                rid=video.rid,
                ep_num=video.ep_num,
                initiate_at=start_time,
                leave_at=end_time_with_delta,
                quality=random.choice(VIDEO_QUALITY_OPTIONS),
                device=random.choice(DEVICE_OPTIONS)
            )

            sessions.append(session_obj)

    return sessions

def create_sessions(viewers: List[Viewer], videos: List[Video]) -> List[Session]:
    sessions = []

    # Generate sessions
    for i in range(NumberOfSessions):
        sid = i + 1  # Sequential session ID

        # Randomly select a viewer and a video
        viewer = random.choice(viewers)
        video = random.choice(videos)

        # Ensure session length does not exceed video length
        session_length = random.randint(1, video.length)

        # Generate random start time
        start_time = faker.date_time_between(start_date=EarliestSessionStartTime, end_date="now")

        # Calculate the end time based on the session length
        end_time = start_time + timedelta(seconds=session_length)

        # Add a random delta (pause) to the end_time
        pause_delta = timedelta(seconds=random.randint(0, 100))
        end_time_with_delta = end_time + pause_delta

        # Create the session
        session_obj = Session(
            sid=sid,
            uid=viewer.uid,
            rid=video.rid,
            ep_num=video.ep_num,
            initiate_at=start_time,
            leave_at=end_time_with_delta,
            quality=random.choice(VIDEO_QUALITY_OPTIONS),
            device=random.choice(DEVICE_OPTIONS)
        )
        sessions.append(session_obj)

    # Add and commit all sessions
    session.add_all(sessions)
    session.commit()

    return sessions

if __name__ == "__main__":
    # Create users, viewers, and producers and insert them into the database
    users, viewers, producers = create_users_producers_viewers()

    # Commit users, viewers, and producers
    session.add_all(users + producers + viewers)
    session.commit()
    print(f"Committed {len(users)} users, {len(viewers)} viewers, {len(producers)} producers")

    # Then create and commit releases, movies, series, and videos
    releases, movies, series_list, videos = create_releases_movies_series_videos(producers)
    session.add_all(releases + movies + series_list + videos)
    session.commit()
    print(f"Committed {len(releases)} releases, {len(movies)} movies, {len(series_list)} series, {len(videos)} videos")

    # Finally, create and commit sessions
    sessions = create_sessions(viewers, videos)
    session.add_all(sessions)
    session.commit()
    print(f"Committed {len(sessions)} sessions")

    print(f"Data generation and insertion completed successfully.")