import random
from faker import Faker
from sql.zot_streaming import User, Producer, Viewer, session
from constants import (
    Seed, NumberOfUsers, NumberOfProducers, EarliestJoinTime, LatestJoinTime,
    GENRES_LIST, VIEWER_SUBSCRIPTION_OPTIONS, NullValueProbability
)

# Initialize Faker with a fixed seed
faker = Faker()
random.seed(Seed)
Faker.seed(Seed)

# List of common email domains
EMAIL_DOMAINS = [
    "gmail.com", "outlook.com", "yahoo.com", "foxmail.com", "icloud.com", "hotmail.com",
    "college.edu", "university.edu", "mail.com", "protonmail.com"
]

def create_users_producers_viewers():
    """
    Generate and return lists of Users, Producers, and Viewers.
    Some users may be both producers and viewers.
    """
    users = []
    viewers = []
    producers = []

    # Generate user attributes in bulk
    nicknames = [faker.user_name() for _ in range(NumberOfUsers)]
    join_dates = [faker.date_between(start_date=EarliestJoinTime, end_date=LatestJoinTime) for _ in range(NumberOfUsers)]
    first_last_names = [(faker.first_name(), faker.last_name()) for _ in range(NumberOfUsers)]

    # Randomly determine overlapping users who are both producers and viewers
    overlap_users = set(random.sample(range(NumberOfUsers), random.randint(1, NumberOfUsers // 2)))

    for i in range(NumberOfUsers):
        user_id = i + 1  # Use sequential integers for user ID

        # Assign random genres (between 1 and 10, following a Gaussian distribution)
        num_genres = int(abs(random.gauss(mu=5, sigma=2)))  # Mean: 5 genres, StdDev: 2
        num_genres = max(1, min(10, num_genres))  # Clamp to range [1, 10]
        user_genres = ','.join(random.sample(GENRES_LIST, k=num_genres))

        # Generate email with a random domain
        email_domain = random.choice(EMAIL_DOMAINS)
        email = f"{nicknames[i]}@{email_domain}"

        # Optional fields: street, city, state, zip (set as NULL based on probability)
        street = faker.street_address() if random.random() > NullValueProbability else None
        city = faker.city() if random.random() > NullValueProbability else None
        state = faker.state() if random.random() > NullValueProbability else None
        zip_code = faker.zipcode() if random.random() > NullValueProbability else None

        # Create User object
        user = User(
            uid=user_id,
            email=email,
            joined_date=join_dates[i],
            nickname=nicknames[i],
            street=street,
            city=city,
            state=state,
            zip=zip_code,
            genres=user_genres,
        )
        users.append(user)

        # Assign producer and viewer roles
        if i < NumberOfProducers or i in overlap_users:
            # Create a producer
            producer = Producer(
                uid=user_id,
                bio=faker.text(max_nb_chars=200),
                company=faker.company() if random.random() > NullValueProbability else None
            )
            producers.append(producer)

        if i >= NumberOfProducers or i in overlap_users:
            # Create a viewer
            first_name, last_name = first_last_names[i]
            viewer = Viewer(
                uid=user_id,
                first_name=first_name,
                last_name=last_name,
                subscription=random.choice(VIEWER_SUBSCRIPTION_OPTIONS),
            )
            viewers.append(viewer)

    return users, viewers, producers


# Example Usage
if __name__ == "__main__":
    # Create users, viewers, and producers and insert them into the database
    users, viewers, producers = create_users_producers_viewers()

    # Commit all users, viewers, and producers to the database
    session.add_all(users + producers + viewers)
    session.commit()
    print(f"Created {len(users)} users, {len(viewers)} viewers, and {len(producers)} producers.")