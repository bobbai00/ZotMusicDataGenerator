# generate users, eiter artist or listener
# dependency:

from utils.generator import *
from sql.zot_music import *
from constants import NumberOfUsers, NumberOfArtists, NumberOfListeners, EarliestJoinTime, LatestJoinTime
def create_users_listeners_artists():
    """
    Generate and return lists of Users, Listeners, and Artists.
    Also inserts them into the database using SQLAlchemy.
    """
    # Initialize empty lists
    users = []
    listeners = []
    artists = []

    # Generate user data
    nicknames = generate_random_nicknames(NumberOfUsers, seed=1234)
    join_dates = generate_random_timestamps(EarliestJoinTime.strftime('%Y-%m-%d'), LatestJoinTime.strftime('%Y-%m-%d'),
                                            NumberOfUsers, seed=1234)
    first_last_names = generate_random_first_last_name_tuples(NumberOfUsers, seed=1234)

    # Generate genres for the users
    genres_per_user = [generate_random_genres(5, seed=1234 + i) for i in range(NumberOfUsers)]

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

        # Add the user's genres
        for genre_name in genres_per_user[i]:
            genre = session.query(Genre).filter_by(genre_name=genre_name).first()
            if genre:
                user.genres.append(genre)

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

    return users, listeners, artists


# Example Usage
if __name__ == "__main__":
    # Create users, listeners, and artists and insert them into the database
    users, listeners, artists = create_users_listeners_artists()
    # Commit all users, listeners, and artists to the database
    session.add_all(users + artists + listeners)
    session.commit()
    print(f"Created {len(users)} users, {len(listeners)} listeners, and {len(artists)} artists.")
