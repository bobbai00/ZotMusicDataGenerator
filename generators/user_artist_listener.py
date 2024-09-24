import uuid
from typing import List
import random
from faker import Faker
from sql.zot_music import User, Listener, Artist, session
from constants import Seed, NumberOfUsers, NumberOfArtists, NumberOfListeners, EarliestJoinTime, LatestJoinTime, \
    GENRES_LIST, LISTENER_SUBSCRIPTION_OPTIONS, generate_unique_id

# Initialize the Faker instance with the seed
faker = Faker()
random.seed(Seed)
Faker.seed(Seed)

# List of common email domains
EMAIL_DOMAINS = [
    "gmail.com", "outlook.com", "yahoo.com", "foxmail.com", "icloud.com", "hotmail.com",
    "college.edu", "university.edu", "mail.com", "protonmail.com"
]

def create_users_listeners_artists() -> (List[User], List[Listener], List[Artist]):
    """
    Generate and return lists of Users, Listeners, and Artists.
    Also inserts them into the database using SQLAlchemy.
    """
    # Initialize empty lists
    users = []
    listeners = []
    artists = []

    # Generate user data using Faker
    nicknames = [faker.user_name() for _ in range(NumberOfUsers)]
    join_dates = [faker.date_between(start_date=EarliestJoinTime, end_date=LatestJoinTime) for _ in range(NumberOfUsers)]
    first_last_names = [(faker.first_name(), faker.last_name()) for _ in range(NumberOfUsers)]

    for i in range(NumberOfUsers):
        user_id = generate_unique_id("user")  # Generate a unique UUID for each user

        # Assign random genres to the user
        user_genres = ','.join(random.sample(GENRES_LIST, k=5))  # Each user gets 5 random genres

        # Randomly pick an email domain from the list
        email_domain = random.choice(EMAIL_DOMAINS)
        email = f'{nicknames[i]}@{email_domain}'

        user = User(
            user_id=user_id,
            email=email,
            joined_date=join_dates[i],
            nickname=nicknames[i],
            street=faker.street_address(),
            city=faker.city(),
            state=faker.state(),
            zip=faker.zipcode(),
            genres=user_genres,
        )
        users.append(user)

        # Create either an artist or a listener
        if i < NumberOfArtists:
            # Create an artist
            artist = Artist(
                user_id=user_id,
                bio=faker.text(max_nb_chars=200),
                stagename=faker.text(max_nb_chars=50).rstrip('.')
            )
            artists.append(artist)
        else:
            # Create a listener
            first_name, last_name = first_last_names[i]
            listener = Listener(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                subscription=random.choice(LISTENER_SUBSCRIPTION_OPTIONS),
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
