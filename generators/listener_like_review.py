from typing import List
import random
from faker import Faker

from generators.listener_review_record import create_reviews
from generators.listener_session_song import create_sessions
from generators.record_single_album_song import create_records_singles_albums_songs
from generators.user_artist_listener import create_users_listeners_artists
from sql.zot_music import ReviewLike, Review, Listener, session
from constants import NumberOfReviewLikes, MinLikesPerReview, MaxLikesPerReview, Seed

# Initialize the Faker instance with the seed
faker = Faker()
random.seed(Seed)
Faker.seed(Seed)

def create_review_likes(reviews: List[Review], listeners: List[Listener]) -> List[ReviewLike]:
    review_likes = []

    for review in reviews:
        # Randomly decide how many likes this review gets (between MinLikesPerReview and MaxLikesPerReview)
        num_likes = random.randint(MinLikesPerReview, MaxLikesPerReview)
        liked_listeners = random.sample(listeners, min(num_likes, len(listeners)))

        for listener in liked_listeners:
            review_like = ReviewLike(
                user_id=listener.user_id,
                review_id=review.review_id
            )
            review_likes.append(review_like)

            # Stop early if the number of likes exceeds the limit
            if len(review_likes) >= NumberOfReviewLikes:
                return review_likes

    return review_likes

# Adjust the main code to commit review likes
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

    # Create review likes and commit them
    review_likes = create_review_likes(reviews, listeners)
    session.add_all(review_likes)
    session.commit()

    print(f"Created {len(users)} users, {len(listeners)} listeners, {len(artists)} artists, {len(records)} records, "
          f"{len(singles)} singles, {len(albums)} albums, {len(songs)} songs, {len(sessions)} sessions, "
          f"{len(reviews)} reviews, {len(review_likes)} review likes.")
