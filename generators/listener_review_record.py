from typing import List
import random
from faker import Faker
from datetime import datetime, timedelta

from generators.listener_session_song import create_sessions
from generators.record_single_album_song import create_records_singles_albums_songs
from generators.user_artist_listener import create_users_listeners_artists
from sql.zot_music import Review, Listener, Record, session
from constants import Seed, generate_unique_id, RecordLatestEndDate, NullValueProbability

# Initialize the Faker instance with the seed
faker = Faker()
random.seed(Seed)
Faker.seed(Seed)

# Function to randomly return None with a certain probability
def random_null(probability=0.2):
    return None if random.random() < probability else True

# Function to generate a rating with Gaussian distribution, clamped between 0 and 5
def generate_gaussian_rating(mean=3.5, std_dev=1.5):
    rating = random.gauss(mean, std_dev)
    return max(0, min(5, rating))  # Clamp the rating between 0 and 5

def create_reviews(listeners: List[Listener], records: List[Record], mean_reviews: int = 10, std_dev: int = 5) -> List[Review]:
    reviews = []

    for record in records:
        # Generate the number of reviews for this record using a Gaussian distribution
        num_reviews = int(abs(random.gauss(mean_reviews, std_dev)))  # Gaussian with mean and std_dev

        # Ensure we have at least 1 review for the record
        num_reviews = max(1, num_reviews)

        # For each review, pick a random listener and generate a review
        for _ in range(num_reviews):
            review_id = generate_unique_id("review")
            listener = random.choice(listeners)  # Randomly pick a listener
            rating = generate_gaussian_rating()  # Gaussian-distributed rating

            # Generate random review body text, but make it occasionally NULL
            if random_null(NullValueProbability):
                review_body = None
            else:
                review_body = faker.text(max_nb_chars=200).replace(",", ' ').replace('\n', ' ').replace("\r", " ")

            # Create the review
            review = Review(
                review_id=review_id,
                user_id=listener.user_id,
                record_id=record.record_id,
                rating=int(rating),  # Convert to int for the final rating
                body=review_body,  # Set the review body, which might be NULL
                posted_at=faker.date_time_between(start_date=RecordLatestEndDate, end_date='now')  # Random timestamp
            )
            reviews.append(review)

    return reviews

# Adjust the main code to commit reviews
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

    print(f"Created {len(users)} users, {len(listeners)} listeners, {len(artists)} artists, {len(records)} records, "
          f"{len(singles)} singles, {len(albums)} albums, {len(songs)} songs, {len(sessions)} sessions, "
          f"{len(reviews)} reviews.")
