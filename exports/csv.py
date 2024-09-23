import csv
import os

from sqlalchemy import inspect

from constants import OutputDir


def save_to_csv(filename, fieldnames, data):
    """
    Write the data to a CSV file in the specified OutputDir with the provided fieldnames.

    :param filename: Name of the CSV file (without directory)
    :param fieldnames: List of field names (CSV headers)
    :param data: List of dictionaries representing rows in the CSV
    """
    os.makedirs(OutputDir, exist_ok=True)  # Ensure the output directory exists
    file_path = os.path.join(OutputDir, filename)

    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"Saved {filename} to {OutputDir}")



def convert_objects_to_dict(objects):
    """
    Convert SQLAlchemy objects to a list of dictionaries for CSV export, using SQLAlchemy's reflection
    to capture only column values and ignore internal states.
    """
    result = []
    for obj in objects:
        # Using the SQLAlchemy inspector to get the column attributes and their values
        obj_dict = {column.key: getattr(obj, column.key) for column in inspect(obj).mapper.column_attrs}
        result.append(obj_dict)
    return result


def export_csvs(users, listeners, artists, records, singles, albums, songs, sessions, reviews, review_likes):
    """
    Export all lists of SQLAlchemy objects to CSV files.
    """
    # Export each table to CSV
    save_to_csv('Users.csv', ['user_id', 'email', 'joined_date', 'nickname', 'street', 'city', 'state', 'zip', 'genres'], convert_objects_to_dict(users))
    save_to_csv('Listeners.csv', ['user_id', 'subscription', 'first_name', 'last_name'], convert_objects_to_dict(listeners))
    save_to_csv('Artists.csv', ['user_id', 'bio'], convert_objects_to_dict(artists))
    save_to_csv('Records.csv', ['record_id', 'artist_user_id', 'title', 'release_date', 'genre'], convert_objects_to_dict(records))
    save_to_csv('Singles.csv', ['record_id', 'video_url'], convert_objects_to_dict(singles))
    save_to_csv('Albums.csv', ['record_id', 'description'], convert_objects_to_dict(albums))
    save_to_csv('Songs.csv', ['record_id', 'track_number', 'title', 'length', 'bpm', 'mood'], convert_objects_to_dict(songs))
    save_to_csv('Sessions.csv', ['session_id', 'user_id', 'record_id', 'track_number', 'initiate_at', 'leave_at', 'music_quality', 'device', 'end_play_time', 'replay_count'], convert_objects_to_dict(sessions))
    save_to_csv('Reviews.csv', ['review_id', 'user_id', 'record_id', 'rating', 'body', 'posted_at'], convert_objects_to_dict(reviews))
    save_to_csv('ReviewLikes.csv', ['user_id', 'review_id'], convert_objects_to_dict(review_likes))
