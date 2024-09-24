from typing import List
import random
from faker import Faker
from datetime import datetime

from generators.user_artist_listener import create_users_listeners_artists
from sql.zot_music import Artist, Record, Single, Album, Song, session
from constants import NumberOfAlbums, NumberOfRecords, NumberOfSingles, MinSongDuration, MaxSongDuration, Seed, \
    RecordEarliestStartDate, RecordLatestEndDate, GENRES_LIST, generate_unique_id

# Initialize the Faker instance with the seed
faker = Faker()
random.seed(Seed)
Faker.seed(Seed)

def create_records_singles_albums_songs(artists: List[Artist]) -> (List[Record], List[Single], List[Album], List[Song]):
    records = []
    singles = []
    albums = []
    songs = []

    # Generate random release dates for records
    release_dates = [faker.date_between(start_date=RecordEarliestStartDate, end_date=RecordLatestEndDate) for _ in range(NumberOfRecords)]

    # Create singles and albums
    for i in range(NumberOfRecords):
        record_id = generate_unique_id("record")
        artist = artists[i % len(artists)]
        release_date = release_dates[i]
        title = faker.sentence(nb_words=3).rstrip('.')  # Generate random song/record title without trailing dot
        chosen_genre = random.sample(GENRES_LIST, 1)[0]  # Random genre selection from list

        if i < NumberOfSingles:
            # Create a single
            single = Single(
                record_id=record_id,
                video_url=faker.url()
            )
            record = Record(
                record_id=record_id,
                artist_user_id=artist.user_id,
                title=title,
                release_date=release_date,
                genre=chosen_genre
            )
            records.append(record)
            singles.append(single)

            # Each single gets exactly 1 song
            song = Song(
                record_id=record_id,
                track_number=1,
                title=title,
                length=random.randint(MinSongDuration, MaxSongDuration),
                bpm=random.randint(60, 180),
                mood=faker.word()
            )
            songs.append(song)
        else:
            # Create an album
            description = faker.text(max_nb_chars=200)  # Generate a random album description
            album = Album(
                record_id=record_id,
                description=description
            )
            record = Record(
                record_id=record_id,
                artist_user_id=artist.user_id,
                title=title,
                release_date=release_date,
                genre=chosen_genre
            )
            records.append(record)
            albums.append(album)

            # Each album gets multiple songs (randomized number between 5 and 12)
            num_songs = random.randint(5, 12)  # Each album has between 5 to 12 songs
            for track_num in range(1, num_songs + 1):
                song_title = faker.sentence(nb_words=3).rstrip('.')  # Generate a random song title without trailing dot
                song = Song(
                    record_id=record_id,
                    track_number=track_num,
                    title=song_title,
                    length=random.randint(MinSongDuration, MaxSongDuration),
                    bpm=random.randint(60, 180),
                    mood=faker.word()
                )
                songs.append(song)

    return records, singles, albums, songs

# Example Usage
if __name__ == "__main__":
    # Create users, listeners, and artists and insert them into the database
    users, listeners, artists = create_users_listeners_artists()

    # Then create records, singles, albums, and songs
    records, singles, albums, songs = create_records_singles_albums_songs(artists)

    session.add_all(users + artists + listeners + records + singles + albums + songs)
    session.commit()
    print(f"Created {len(users)} users, {len(listeners)} listeners, {len(artists)} artists, {len(records)} records, {len(singles)} singles, {len(albums)} albums, {len(songs)} songs")
