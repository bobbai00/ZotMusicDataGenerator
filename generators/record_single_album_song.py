from typing import List
import random
from faker import Faker
from datetime import datetime

from generators.user_artist_listener import create_genres_users_listeners_artists
from sql.zot_music import Artist, Record, Single, Album, Song, Genre, session
from constants import NumberOfAlbums, NumberOfRecords, NumberOfSingles, MinSongDuration, MaxSongDuration, Seed, \
    RecordEarliestStartDate, RecordLatestEndDate

# Initialize the Faker instance with the seed
faker = Faker()
random.seed(Seed)
Faker.seed(Seed)

def create_records_singles_albums_songs(genres: List[Genre], artists: List[Artist]) -> (List[Record], List[Single], List[Album], List[Song]):
    records = []
    singles = []
    albums = []
    songs = []

    # Generate random release dates for records
    release_dates = [faker.date_between(start_date=RecordEarliestStartDate, end_date=RecordLatestEndDate) for _ in range(NumberOfRecords)]

    # Create singles and albums
    for i in range(NumberOfRecords):
        record_id = f'record_{i + 1}'
        artist = artists[i % len(artists)]
        release_date = release_dates[i]
        title = faker.sentence(nb_words=3)  # Generate random song/record title

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
                release_date=release_date
            )
            records.append(record)
            singles.append(single)

            # Assign random genres to the record
            assign_random_genres(record, genres)

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
                release_date=release_date
            )
            records.append(record)
            albums.append(album)

            # Assign random genres to the album
            assign_random_genres(record, genres)

            # Each album gets multiple songs (randomized number between 5 and 12)
            num_songs = random.randint(5, 12)  # Each album has between 5 to 12 songs
            for track_num in range(1, num_songs + 1):
                song_title = faker.sentence(nb_words=3)  # Generate a random song title
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


def assign_random_genres(record: Record, all_genres: List[Genre]):
    """
    Assign random genres to a record.
    :param record: The Record object
    :param all_genres: List of all available genres
    """
    num_genres = random.randint(1, 3)  # Each record can have 1 to 3 genres
    chosen_genres = random.sample(all_genres, num_genres)
    for genre in chosen_genres:
        record.genres.append(genre)


# Example Usage
if __name__ == "__main__":
    # Create users, listeners, and artists and insert them into the database
    genres, users, listeners, artists = create_genres_users_listeners_artists()

    # Then create records, singles, albums, and songs
    records, singles, albums, songs = create_records_singles_albums_songs(genres, artists)

    session.add_all(users + artists + listeners + records + singles + albums + songs)
    session.commit()
    print(f"Created {len(users)} users, {len(listeners)} listeners, {len(artists)} artists, {len(records)} records, {len(singles)} singles, {len(albums)} albums, {len(songs)} songs")
