from typing import List
import random
from faker import Faker
from datetime import datetime, timedelta

from generators.record_single_album_song import create_records_singles_albums_songs
from generators.user_artist_listener import create_users_listeners_artists
from sql.zot_music import Song, Session, Listener, session
from constants import NumberOfSessions, EarliestSessionStartTime, Seed, MUSIC_QUALITY_OPTIONS, DEVICE_OPTIONS, \
    generate_unique_id

# Initialize Faker with seed
faker = Faker()
random.seed(Seed)
Faker.seed(Seed)

def create_sessions(listeners: List[Listener], songs: List[Song]) -> List[Session]:
    sessions = []

    # Generate sessions
    for i in range(NumberOfSessions):
        session_id = generate_unique_id("session")

        # Randomly select a listener and a song for this session
        listener = random.choice(listeners)
        song = random.choice(songs)

        # Ensure the session length is no longer than the song length
        session_length = random.randint(1, song.length)  # The session length can't exceed the song's length (in seconds)

        # Generate random start time
        start_time = faker.date_time_between(start_date=EarliestSessionStartTime, end_date="now")

        # Calculate the end time based on the session length
        end_time = start_time + timedelta(seconds=session_length)

        # Add a random delta (pause) to the end_time
        pause_delta = timedelta(seconds=random.randint(0, 100))  # Random pause between 1 and 30 seconds
        end_time_with_delta = end_time + pause_delta

        # Create the session
        session_obj = Session(
            session_id=session_id,
            user_id=listener.user_id,
            record_id=song.record_id,
            track_number=song.track_number,
            initiate_at=start_time,
            leave_at=end_time_with_delta,  # Using the end time with added delta (pause)
            music_quality=random.choice(MUSIC_QUALITY_OPTIONS),
            device=random.choice(DEVICE_OPTIONS),
            remaining_time=session_length,
            replay_count=random.randint(0, 5)  # Random replay count
        )
        sessions.append(session_obj)

    # Add and commit all sessions
    session.add_all(sessions)
    session.commit()

    return sessions

if __name__ == "__main__":
    # Create genres, users, listeners, and artists and insert them into the database
    users, listeners, artists = create_users_listeners_artists()

    # Commit users, listeners, and artists
    session.add_all(users + artists + listeners)
    session.commit()
    print(f"Committed {len(users)} users, {len(listeners)} listeners, {len(artists)} artists")

    # Then create and commit records, singles, albums, and songs
    records, singles, albums, songs = create_records_singles_albums_songs(artists)
    session.add_all(records + singles + albums + songs)
    session.commit()
    print(f"Committed {len(records)} records, {len(singles)} singles, {len(albums)} albums, {len(songs)} songs")

    # Finally, create and commit sessions
    sessions = create_sessions(listeners, songs)
    session.add_all(sessions)
    session.commit()
    print(f"Committed {len(sessions)} sessions")

    print(f"Data generation and insertion completed successfully.")

