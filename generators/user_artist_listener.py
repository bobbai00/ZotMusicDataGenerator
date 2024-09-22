from typing import List
import random
from faker import Faker
from sql.zot_music import User, Listener, Artist, Genre, UserGenres, session
from constants import Seed, NumberOfUsers, NumberOfArtists, NumberOfListeners, EarliestJoinTime, LatestJoinTime

# Initialize the Faker instance with the seed
faker = Faker()
random.seed(Seed)
Faker.seed(Seed)

# Fixed set of 20 unique genre names
GENRES_LIST = [
    'Rock', 'Pop', 'Hip-Hop', 'Jazz', 'Classical', 'Electronic',
    'Country', 'Reggae', 'Blues', 'Folk', 'Soul', 'Metal',
    'Punk', 'Disco', 'Latin', 'Funk', 'Indie', 'R&B',
    'Gospel', 'Techno'
]

def create_genres_users_listeners_artists() -> (List[Genre], List[User], List[Listener], List[Artist]):
    """
    Generate and return lists of Genres, Users, Listeners, and Artists.
    Also inserts them into the database using SQLAlchemy.
    """
    # Initialize empty lists
    genres = []
    users = []
    listeners = []
    artists = []

    # Insert genres into the database
    for genre_name in GENRES_LIST:
        genre = Genre(genre_name=genre_name)
        genres.append(genre)

    # Commit the genres to the database
    session.add_all(genres)
    session.commit()

    # Retrieve the genres from the database to ensure consistency
    all_genres = session.query(Genre).all()

    # Generate user data using Faker
    nicknames = [faker.user_name() for _ in range(NumberOfUsers)]
    join_dates = [faker.date_between(start_date=EarliestJoinTime, end_date=LatestJoinTime) for _ in range(NumberOfUsers)]
    first_last_names = [(faker.first_name(), faker.last_name()) for _ in range(NumberOfUsers)]

    for i in range(NumberOfUsers):
        user_id = f'user_{i + 1}'
        user = User(
            user_id=user_id,
            email=f'{nicknames[i]}@example.com',
            joined_date=join_dates[i],
            nickname=nicknames[i],
            street=faker.street_address(),
            city=faker.city(),
            state=faker.state(),
            zip=faker.zipcode()
        )
        users.append(user)

        # Assign random genres to the user
        user_genres = random.sample(all_genres, k=5)  # Each user gets 5 random genres
        for genre in user_genres:
            user.genres.append(genre)  # Add genres through the relationship

        # Create either an artist or a listener
        if i < NumberOfArtists:
            # Create an artist
            artist = Artist(
                user_id=user_id,
                bio=faker.text(max_nb_chars=200)
            )
            artists.append(artist)
        else:
            # Create a listener
            first_name, last_name = first_last_names[i]
            listener = Listener(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                subscription=random.choice(['free', 'monthly', 'yearly'])
            )
            listeners.append(listener)

    return genres, users, listeners, artists


# Example Usage
if __name__ == "__main__":
    # Create genres, users, listeners, and artists and insert them into the database
    genres, users, listeners, artists = create_genres_users_listeners_artists()

    # Commit all users, listeners, and artists to the database
    session.add_all(users + artists + listeners)
    session.commit()
    print(f"Created {len(genres)} genres, {len(users)} users, {len(listeners)} listeners, and {len(artists)} artists.")
