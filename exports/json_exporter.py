import csv
import os
from datetime import datetime

import psycopg2
import json
import random

RANDOM_SEED = 42

def shuffle_list(data_list):
    random.seed(RANDOM_SEED)
    random.shuffle(data_list)
    return data_list

# Database connection
conn = psycopg2.connect(
    dbname="baijiadong",
    user="baijiadong",
    password="123456",
    host="localhost",
    port="5432"
)

# Cursor for executing queries
cur = conn.cursor()
cur.execute("SET search_path TO zotmusic;")

target_dir = './results/zot-music-dataset-assignment6'

def get_target_path(filename, is_jsonl):
    suffix = ".jsonl" if is_jsonl else ".json"
    return os.path.join(target_dir, f"{filename}{suffix}")

def omit_null_fields(data):
    if isinstance(data, dict):
        return {k: omit_null_fields(v) for k, v in data.items() if v is not None}
    return data

# New function to write all data as a JSON array or JSON Lines
def write_json_array(data, filename, is_jsonl=False):
    file_path = get_target_path(filename, is_jsonl)
    with open(file_path, 'w') as f:
        if is_jsonl:
            for item in data:
                f.write(json.dumps(item) + "\n")
        else:
            json.dump(data, f, indent=2)

# 1. Transform Users Data
def transform_users():
    cur.execute("""
        SELECT 
            u.user_id, u.email, u.joined_date, u.nickname, 
            u.street, u.city, u.state, u.zip, 
            string_to_array(u.genres, ',') AS genres,
            (a.user_id IS NOT NULL) AS is_artist,
            (l.user_id IS NOT NULL) AS is_listener,
            l.subscription,
            l.first_name, l.last_name,
            a.stagename, a.bio
        FROM Users u
        LEFT JOIN Artists a ON u.user_id = a.user_id
        LEFT JOIN Listeners l ON u.user_id = l.user_id
    """)
    users = []
    for row in cur.fetchall():
        is_listener = row[10]
        is_artist = row[9]

        user = {
            "user_id": row[0],
            "email": row[1],
            "joined_date": str(row[2]),
            "nickname": row[3],
            "address": {
                "street": row[4],
                "city": row[5],
                "state": row[6],
                "zip": row[7]
            },
            "genres": [genre for genre in row[8] if genre] if row[8] else [],
            "is_listener": is_listener,
            "is_artist": is_artist
        }

        if is_listener:
            user["subscription"] = row[11]

        if row[12] or row[13]:
            user["real_name"] = {
                "first_name": row[12],
                "last_name": row[13]
            }

        if is_artist:
            user["stage_name"] = row[14]
            user["bio"] = row[15]

        users.append(omit_null_fields(user))

    users = shuffle_list(users)
    write_json_array(users, "Users", is_jsonl=True)

# 2. Transform Records Data
def transform_records():
    cur.execute("""
        SELECT 
            r.record_id, r.title, r.genre, r.release_date, 
            r.artist_user_id, 
            (al.record_id IS NOT NULL) AS is_album, 
            (si.record_id IS NOT NULL) AS is_single, 
            al.description, si.video_url
        FROM Records r
        LEFT JOIN Albums al ON r.record_id = al.record_id
        LEFT JOIN Singles si ON r.record_id = si.record_id
    """)

    records = []
    for row in cur.fetchall():
        artist_id = row[4]

        record = {
            "record_id": row[0],
            "title": row[1],
            "genre": row[2],
            "released_by": {
                "artist_user_id": artist_id,
                "release_date": str(row[3]) if row[3] else None
            },
            "is_album": row[5],
            "is_single": row[6]
        }

        if row[7]:
            record["description"] = row[7]
        if row[8]:
            record["video_url"] = row[8]

        cur.execute("""
            SELECT track_number, title, length, bpm, mood 
            FROM Songs 
            WHERE record_id = %s
            ORDER BY track_number
        """, (row[0],))
        record["songs"] = [
            omit_null_fields(
                {k: v for k, v in zip(["track_number", "title", "length", "bpm", "mood"], song)}
            )
            for song in cur.fetchall()
        ]

        records.append(omit_null_fields(record))

    records = shuffle_list(records)
    write_json_array(records, "Records", is_jsonl=True)

# 3. Transform Reviews Data
def transform_reviews():
    cur.execute("""
        SELECT review_id, user_id, record_id, rating, body, posted_at 
        FROM Reviews
    """)
    reviews = []
    for row in cur.fetchall():
        review = {
            "review_id": row[0],
            "posted_by": {
                "user_id": row[1],
                "posted_time": str(row[5])
            },
            "record_id": row[2],
            "rating": row[3],
            "body": row[4]
        }
        reviews.append(omit_null_fields(review))

    write_json_array(reviews, "Reviews", is_jsonl=True)

# 4. Transform Sessions Data
def transform_sessions():
    cur.execute("""
        SELECT 
            session_id, user_id, record_id, track_number, initiate_at, 
            leave_at, music_quality, device, remaining_time, replay_count 
        FROM Sessions
    """)
    sessions = []
    for row in cur.fetchall():
        session = {
            "session_id": row[0],
            "user_id": row[1],
            "song": {
                "record_id": row[2],
                "track_number": row[3]
            },
            "session_duration": {
                "initiate_at": str(row[4]),
                "leave_at": str(row[5])
            },
            "music_quality": row[6],
            "device": row[7],
            "remaining_time": row[8],
            "replay_count": row[9]
        }
        sessions.append(omit_null_fields(session))

    # Sort sessions by session_duration.initiate_at (in ascending order)
    sessions.sort(key=lambda x: datetime.strptime(x["session_duration"]["initiate_at"], "%Y-%m-%d %H:%M:%S"))
    write_json_array(sessions, "Sessions", is_jsonl=True)

# 5. Transform ReviewLikes Data
def transform_reviewlikes():
    cur.execute("SELECT user_id, review_id FROM ReviewLikes")
    reviewlikes = [{"user_id": row[0], "review_id": row[1]} for row in cur.fetchall()]
    write_json_array(reviewlikes, "ReviewLikes", is_jsonl=True)

# Call transformation functions
transform_users()
transform_records()
transform_reviews()
transform_sessions()
transform_reviewlikes()

# Close connection
cur.close()
conn.close()