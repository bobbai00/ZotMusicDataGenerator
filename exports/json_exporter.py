import psycopg2
import json

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
# Set search path to zotmusic schema
cur.execute("SET search_path TO zotmusic;")
# Helper function to check if value is None and skip it
def skip_null(value):
    return value if value is not None else None

# 1. Transform Users Data
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
        # Handle listener and artist conditions
        is_listener = row[10]
        is_artist = row[9]

        user = {
            "user_id": row[0],
            "email": row[1],
            "joined_date": str(row[2]),
            "nickname": row[3],
            "address": {key: value for key, value in zip(["street", "city", "state", "zip"], row[4:8]) if value},
            "genres": [genre for genre in row[8] if genre] if row[8] else [],
            "is_listener": is_listener,
            "is_artist": is_artist
        }

        # Include subscription details for listeners
        if is_listener:
            user["subscription"] = row[11]

        # Include real name for listeners
        if row[12] or row[13]:
            user["real_name"] = {k: v for k, v in zip(["first_name", "last_name"], row[12:14]) if v}

        # Include stage name and bio for artists (if they are also artists)
        if is_artist:
            if row[14]:
                user["stage_name"] = row[14]
            if row[15]:
                user["bio"] = row[15]

        users.append(user)

    # Write to JSON
    with open("Users.json", "w") as f:
        json.dump(users, f, indent=2)


def transform_records():
    cur.execute("""
        SELECT 
            r.record_id, r.title, r.genre, r.release_date, 
            r.artist_user_id, a.stagename, 
            (al.record_id IS NOT NULL) AS is_album, 
            (si.record_id IS NOT NULL) AS is_single, 
            al.description, si.video_url
        FROM Records r
        LEFT JOIN Albums al ON r.record_id = al.record_id
        LEFT JOIN Singles si ON r.record_id = si.record_id
        LEFT JOIN Artists a ON r.artist_user_id = a.user_id
    """)

    records = []
    for row in cur.fetchall():
        artist_id = row[4]  # Use artist_user_id instead of stagename for the artist field

        # Check if there is a stage name; use it if available, otherwise fallback to artist_id
        artist_name = artist_id

        record = {
            "record_id": row[0],
            "title": row[1],
            "genre": row[2],
            "released_by": {"artist": artist_name, "release_date": str(row[3])} if row[3] else {"artist": artist_name},
            "is_album": row[6],
            "is_single": row[7]
        }

        if row[8]:
            record["description"] = row[8]
        if row[9]:
            record["video_url"] = row[9]

        # Fetch associated songs
        cur.execute("""
            SELECT track_number, title, length, bpm, mood 
            FROM Songs 
            WHERE record_id = %s
            ORDER BY track_number
        """, (row[0],))
        record["songs"] = [
            {k: v for k, v in zip(["track_number", "title", "length", "bpm", "mood"], song) if v}
            for song in cur.fetchall()
        ]

        records.append(record)

    with open("Records.json", "w") as f:
        json.dump(records, f, indent=2)

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
            "posted_by": {"user_id": row[1], "posted_time": str(row[5])},
            "record_id": row[2],
            "rating": row[3]
        }
        if row[4]:
            review["body"] = row[4]
        reviews.append(review)
    with open("Reviews.json", "w") as f:
        json.dump(reviews, f, indent=2)

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
            "song": {"record_id": row[2], "track_number": row[3]},
            "session_duration": {"initiate_at": str(row[4]), "leave_at": str(row[5])},
            "music_quality": row[6],
            "device": row[7],
            "remaining_time": row[8]
        }
        if row[9] is not None:
            session["replay_count"] = row[9]
        sessions.append(session)
    with open("Sessions.json", "w") as f:
        json.dump(sessions, f, indent=2)

# 5. Transform ReviewLikes Data
def transform_reviewlikes():
    cur.execute("SELECT user_id, review_id FROM ReviewLikes")
    reviewlikes = [{"user_id": row[0], "review_id": row[1]} for row in cur.fetchall()]
    with open("ReviewLikes.json", "w") as f:
        json.dump(reviewlikes, f, indent=2)

# Call transformation functions
transform_users()
transform_records()
transform_reviews()
transform_sessions()
transform_reviewlikes()

# Close connection
cur.close()
conn.close()