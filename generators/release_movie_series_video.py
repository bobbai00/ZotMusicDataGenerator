from typing import List
import random
from faker import Faker
from datetime import datetime

from generators.user_producer_viewer import create_users_producers_viewers
from sql.zot_streaming import Producer, Release, Movie, Series, Video, session
from constants import (
    NumberOfReleases, NumberOfMovies, MinVideoDuration, MaxVideoDuration, Seed,
    ReleaseEarliestStartDate, ReleaseLatestEndDate, GENRES_LIST, NullValueProbability
)

# Initialize Faker with a fixed seed
faker = Faker()
random.seed(Seed)
Faker.seed(Seed)

# Function to randomly return None with a certain probability
def random_null(probability=NullValueProbability):
    return None if random.random() < probability else True

# Function to generate video length using a Gaussian distribution
def generate_gaussian_length(min_length, max_length, mean=None, std_dev=None):
    mean = mean if mean is not None else (min_length + max_length) / 2  # Default mean is midpoint
    std_dev = std_dev if std_dev is not None else (max_length - min_length) / 6  # Covers 99.7% within bounds
    length = abs(random.gauss(mean, std_dev))  # Gaussian distribution
    return int(max(min_length, min(max_length, length)))  # Clamp within range

def create_releases_movies_series_videos(producers: List[Producer]) -> (List[Release], List[Movie], List[Series], List[Video]):
    releases = []
    movies = []
    series_list = []
    videos = []

    # Generate random release dates
    release_dates = [faker.date_between(start_date=ReleaseEarliestStartDate, end_date=ReleaseLatestEndDate) for _ in range(NumberOfReleases)]

    for i in range(NumberOfReleases):
        rid = i + 1  # Use sequential integers for release ID
        producer = producers[i % len(producers)]
        title = faker.sentence(nb_words=3).rstrip('.')  # Random release title
        chosen_genre = random.choice(GENRES_LIST)  # Random genre selection
        release_date = release_dates[i]

        # Create a release
        release = Release(
            rid=rid,
            producer_uid=producer.uid,
            title=title,
            release_date=release_date,
            genre=chosen_genre
        )
        releases.append(release)

        if i < NumberOfMovies:
            # Create a movie
            movie = Movie(
                rid=rid,
                website_url=faker.url()
            )
            movies.append(movie)
        else:
            # Create a series
            introduction = faker.text(max_nb_chars=200) if random_null(probability=NullValueProbability) else None
            series = Series(
                rid=rid,
                introduction=introduction
            )
            series_list.append(series)

            # Generate episodes for the series (randomized number between 5 and 12)
            num_episodes = random.randint(5, 12)
            for ep_num in range(1, num_episodes + 1):
                episode_title = faker.sentence(nb_words=3).rstrip('.')
                video = Video(
                    rid=rid,
                    ep_num=ep_num,
                    title=episode_title,
                    length=generate_gaussian_length(MinVideoDuration, MaxVideoDuration)
                )
                videos.append(video)

    return releases, movies, series_list, videos

# Example Usage
if __name__ == "__main__":
    # Create users, viewers, and producers and insert them into the database
    users, viewers, producers = create_users_producers_viewers()

    # Then create releases, movies, series, and videos
    releases, movies, series_list, videos = create_releases_movies_series_videos(producers)

    session.add_all(users + producers + viewers + releases + movies + series_list + videos)
    session.commit()
    print(f"Created {len(users)} users, {len(viewers)} viewers, {len(producers)} producers, {len(releases)} releases, {len(movies)} movies, {len(series_list)} series, {len(videos)} videos.")