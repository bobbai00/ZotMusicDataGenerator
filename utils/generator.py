import random
from faker import Faker
from datetime import datetime, timedelta

from constants import MinSongDuration, MaxSongDuration

# Initialize the Faker instance
faker = Faker()


def generate_random_song_titles(num, seed):
    """
    Generate a list of random song titles.

    :param num: Number of titles to generate
    :param seed: Random seed for reproducibility
    :return: List of random song titles
    """
    random.seed(seed)
    Faker.seed(seed)
    return [faker.catch_phrase() for _ in range(num)]


def generate_random_record_descriptions(num, seed):
    """
    Generate a list of random record descriptions.

    :param num: Number of descriptions to generate
    :param seed: Random seed for reproducibility
    :return: List of random record descriptions
    """
    random.seed(seed)
    Faker.seed(seed)
    return [faker.text(max_nb_chars=200) for _ in range(num)]


def generate_random_nicknames(num, seed):
    """
    Generate a list of random nicknames.

    :param num: Number of nicknames to generate
    :param seed: Random seed for reproducibility
    :return: List of random nicknames
    """
    random.seed(seed)
    Faker.seed(seed)
    return [faker.user_name() for _ in range(num)]


def generate_random_first_last_name_tuples(num, seed):
    """
    Generate a list of random (first name, last name) tuples.

    :param num: Number of tuples to generate
    :param seed: Random seed for reproducibility
    :return: List of tuples containing (first_name, last_name)
    """
    random.seed(seed)
    Faker.seed(seed)
    return [(faker.first_name(), faker.last_name()) for _ in range(num)]


# Fixed set of 20 unique genre names
GENRES_LIST = [
    'Rock', 'Pop', 'Hip-Hop', 'Jazz', 'Classical', 'Electronic',
    'Country', 'Reggae', 'Blues', 'Folk', 'Soul', 'Metal',
    'Punk', 'Disco', 'Latin', 'Funk', 'Indie', 'R&B',
    'Gospel', 'Techno'
]

def generate_random_genres(num, seed):
    """
    Generate a list of unique random genres from a fixed set of 20 genre names.

    :param num: Number of unique genres to generate (must be <= 20)
    :param seed: Random seed for reproducibility
    :return: List of unique random genres
    """
    if num > 20:
        raise ValueError("Number of genres requested exceeds the available set of 20 unique genres.")

    random.seed(seed)

    # Randomly select 'num' unique genres from the GENRES_LIST
    return random.sample(GENRES_LIST, num)


def generate_start_end_timestamps(no_later_than, num, seed):
    """
    Generate a list of (start_timestamp, end_timestamp) tuples with random intervals.

    :param no_later_than: Latest possible end timestamp (as a datetime object)
    :param num: Number of tuples to generate
    :param seed: Random seed for reproducibility
    :return: List of (start_timestamp, end_timestamp) tuples
    """
    random.seed(seed)

    result = []

    for _ in range(num):
        # Generate a random interval between 120 and 360 seconds
        interval = timedelta(seconds=random.randint(MinSongDuration, MaxSongDuration))

        # Generate a random end timestamp that is no later than `no_later_than`
        end_timestamp = no_later_than - timedelta(seconds=random.randint(0, int(interval.total_seconds())))

        # Calculate the start timestamp by subtracting the interval from the end timestamp
        start_timestamp = end_timestamp - interval

        # Append the (start, end) tuple to the result list
        result.append((start_timestamp, end_timestamp))

    return result


def generate_random_timestamps(earliest, latest, num, seed):
    """
    Generate a list of random timestamps between two dates.

    :param earliest: Earliest date (string in 'YYYY-MM-DD' format)
    :param latest: Latest date (string in 'YYYY-MM-DD' format)
    :param num: Number of timestamps to generate
    :param seed: Random seed for reproducibility
    :return: List of random timestamps as datetime objects
    """
    random.seed(seed)

    # Convert earliest and latest to datetime objects
    earliest_date = datetime.strptime(earliest, '%Y-%m-%d')
    latest_date = datetime.strptime(latest, '%Y-%m-%d')

    # Ensure latest_date is later than earliest_date
    if latest_date < earliest_date:
        raise ValueError("Latest date must be later than or equal to earliest date.")

    # Get timestamps for earliest and latest dates
    earliest_timestamp = earliest_date.timestamp()
    latest_timestamp = latest_date.timestamp()

    # Generate random timestamps between the earliest and latest
    return [datetime.fromtimestamp(random.uniform(earliest_timestamp, latest_timestamp)) for _ in range(num)]


# Example Usage
if __name__ == "__main__":
    # Generate 5 random song titles
    print(generate_random_song_titles(5, 1234))

    # Generate 5 random record descriptions
    print(generate_random_record_descriptions(5, 1234))

    # Generate 5 random nicknames
    print(generate_random_nicknames(5, 1234))

    # Generate 5 random (first name, last name) tuples
    print(generate_random_first_last_name_tuples(5, 1234))
