from typing import List
import random
from faker import Faker
from datetime import datetime, timedelta

from generators.viewer_session_video import create_sessions
from generators.release_movie_series_video import create_releases_movies_series_videos
from generators.user_producer_viewer import create_users_producers_viewers
from sql.zot_streaming import Review, Viewer, Release, session
from constants import Seed, ReleaseLatestEndDate, NullValueProbability

# Initialize Faker with seed
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

def create_reviews(viewers: List[Viewer], releases: List[Release], mean_reviews: int = 10, std_dev: int = 5) -> List[Review]:
    reviews = []
    trimmed_viewers = viewers[:-10]  # Reduce available reviewers for variety

    for release in releases:
        # Generate the number of reviews for this release using a Gaussian distribution
        num_reviews = int(abs(random.gauss(mean_reviews, std_dev)))

        # Ensure at least 1 review per release
        num_reviews = max(1, num_reviews)

        for _ in range(num_reviews):
            rvid = len(reviews) + 1  # Sequential review ID
            viewer = random.choice(trimmed_viewers)  # Randomly pick a viewer
            rating = generate_gaussian_rating()  # Gaussian-distributed rating

            # Generate random review body text, but make it occasionally NULL
            review_body = None if random_null(NullValueProbability) else faker.text(max_nb_chars=200)

            # Create the review
            review = Review(
                rvid=rvid,
                uid=viewer.uid,
                rid=release.rid,
                rating=int(rating),  # Convert to int for the final rating
                body=review_body,  # Review body, can be NULL
                posted_at=faker.date_time_between(start_date=ReleaseLatestEndDate, end_date='now')  # Random timestamp
            )
            reviews.append(review)

    return reviews

if __name__ == "__main__":
    # Create users, viewers, and producers and insert them into the database
    users, viewers, producers = create_users_producers_viewers()

    # Commit users, viewers, and producers
    session.add_all(users + producers + viewers)
    session.commit()

    # Create releases, movies, series, and videos
    releases, movies, series_list, videos = create_releases_movies_series_videos(producers)

    # Commit releases, movies, series, and videos
    session.add_all(releases + movies + series_list + videos)
    session.commit()

    # Create sessions and commit them
    sessions = create_sessions(viewers, videos)
    session.add_all(sessions)
    session.commit()

    # Create reviews and commit them
    reviews = create_reviews(viewers, releases)
    session.add_all(reviews)
    session.commit()

    print(f"Created {len(users)} users, {len(viewers)} viewers, {len(producers)} producers, {len(releases)} releases, "
          f"{len(movies)} movies, {len(series_list)} series, {len(videos)} videos, {len(sessions)} sessions, "
          f"{len(reviews)} reviews.")