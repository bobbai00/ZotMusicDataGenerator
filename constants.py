import base64
from datetime import datetime
import uuid

# required
TargetFormat = "csv"
# required
OutputDir = "./results/zot-music-dataset-small"
# required
MySQLDBUrl = 'mysql+pymysql://root:123456@localhost'
# required
DBName = 'ZotMusicMysql'

# Fixed set of 20 unique genre names
GENRES_LIST = [
    'Rock', 'Pop', 'Hip-Hop', 'Jazz', 'Classical', 'Electronic',
    'Country', 'Reggae', 'Blues', 'Folk', 'Soul', 'Metal',
    'Punk', 'Disco', 'Latin', 'Funk', 'Indie', 'R&B',
    'Gospel', 'Techno'
]
MUSIC_QUALITY_OPTIONS = ["lowest", "low", "normal", "high", "Hi-Fi", "lossless"]
DEVICE_OPTIONS = ["mobile-browser", "mobile-app", "desktop-browser", "desktop-app"]
LISTENER_SUBSCRIPTION_OPTIONS = ["free", "monthly", "yearly"]

Seed = 1234
NullValueProbability = 0.2

# Users
NumberOfUsers = 5000
PortionOfArtists = 20  # 10% to 30% (adjustable)
NumberOfArtists = int(PortionOfArtists * NumberOfUsers // 100)
EarliestJoinTime = datetime(2015, 1, 1)
LatestJoinTime = datetime(2023, 1, 1)

# Records
NumberOfRecords = 20000
PortionOfSingles = 30  # 1% to 50% of records are singles
NumberOfSingles = int(PortionOfSingles * NumberOfRecords // 100)
NumberOfAlbums = NumberOfRecords - NumberOfSingles
RecordEarliestStartDate = datetime(2020, 1, 1)
RecordLatestEndDate = datetime(2024, 1, 1)

# Songs
MinSongDuration = 60  # 2 minutes # normal distri
MaxSongDuration = 600  # 6 minutes

# Sessions
NumberOfSessions = 2000000
EarliestSessionStartTime = datetime(2023, 1, 2)

# Reviews


# Review Likes
# 0 - 500 per record

def generate_unique_id(prefix: str) -> str:
    """Generate a short unique ID with a given prefix."""
    short_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode('utf-8').rstrip("=")[:12]
    return f"{prefix}_{short_uuid}"