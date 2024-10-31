import pandas as pd
import os

# Directory where your CSV files are stored
data_dir = './results/zot-music-dataset-small'
target_dir = './results/zot-music-dataset-assignment4'

# Ensure target directory exists
os.makedirs(target_dir, exist_ok=True)

# Load each entity CSV file
users_df = pd.read_csv(os.path.join(data_dir, 'Users.csv'))
listeners_df = pd.read_csv(os.path.join(data_dir, 'Listeners.csv'))
artists_df = pd.read_csv(os.path.join(data_dir, 'Artists.csv'))
records_df = pd.read_csv(os.path.join(data_dir, 'Records.csv'))
reviews_df = pd.read_csv(os.path.join(data_dir, 'Reviews.csv'))
review_likes_df = pd.read_csv(os.path.join(data_dir, 'ReviewLikes.csv'))
albums_df = pd.read_csv(os.path.join(data_dir, 'Albums.csv'))
singles_df = pd.read_csv(os.path.join(data_dir, 'Singles.csv'))

# 1. Process Users - Save to target without modifications
users_df.to_csv(os.path.join(target_dir, 'Users.csv'), index=False)

# 2. Process Listeners - Keep `user_id` column to relate to Users
listeners_df.to_csv(os.path.join(target_dir, 'Listeners.csv'), index=False)

# 3. Process Artists - Keep `user_id` column to relate to Users
artists_df.to_csv(os.path.join(target_dir, 'Artists.csv'), index=False)

# 4. Generate Relationship CSVs in the target directory

# Artists Releases Record - Extract relationship columns
artists_releases_record = records_df[['artist_user_id', 'record_id', 'release_date']]
artists_releases_record.to_csv(os.path.join(target_dir, 'Artists_Releases_Record.csv'), index=False)

# Users Post Reviews - Extract relationship columns from Reviews
users_post_reviews = reviews_df[['user_id', 'review_id', 'posted_at']]
users_post_reviews.to_csv(os.path.join(target_dir, 'Users_Post_Reviews.csv'), index=False)

# Reviews About Record - Extract relationship columns from Reviews
reviews_about_record = reviews_df[['review_id', 'record_id']]
reviews_about_record.to_csv(os.path.join(target_dir, 'Reviews_About_Record.csv'), index=False)

# Upvotes (Likes) - Extract relationship columns from ReviewLikes
upvotes = review_likes_df[['user_id', 'review_id']]
upvotes.to_csv(os.path.join(target_dir, 'Upvotes.csv'), index=False)

# 5. Process Records - Only remove `artist_user_id` as it's been used for relationship extraction
records_df = records_df.drop(columns=['artist_user_id', 'release_date'])
records_df.to_csv(os.path.join(target_dir, 'Records.csv'), index=False)

# 6. Process Albums and Singles - Save to target without modification to relate with Records
albums_df.to_csv(os.path.join(target_dir, 'Albums.csv'), index=False)
singles_df.to_csv(os.path.join(target_dir, 'Singles.csv'), index=False)

# 7. Process Reviews - Save to target without modifications
reviews_df = reviews_df.drop(columns=['user_id', 'posted_at', 'record_id'])
reviews_df.to_csv(os.path.join(target_dir, 'Reviews.csv'), index=False)

print("Processed entity and relationship CSVs have been created successfully in the target directory!")
