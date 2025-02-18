import base64
from datetime import datetime
import uuid

# required
TargetFormat = "csv"
# required
OutputDir = "./results/zot-streaming-dataset-small"
# required
MySQLDBUrl = 'mysql+pymysql://root:123456@localhost'
# required
DBName = 'cs122a_hw2'

# Fixed set of 20 unique genre names
GENRES_LIST = [
    "Action", "Adventure", "Comedy", "Drama", "Horror", "Thriller", "Mystery",
    "Sci-Fi", "Fantasy", "Romance", "Animation", "Crime", "Musical", "Documentary",
    "War", "Western", "Historical", "Sports", "Family", "Biography"
]
VIDEO_QUALITY_OPTIONS = ['480p', '720p', '1080p']
DEVICE_OPTIONS = ['mobile', 'desktop']
VIEWER_SUBSCRIPTION_OPTIONS = ["free", "monthly", "yearly"]

Seed = 1234
NullValueProbability = 0.2

# Users
NumberOfUsers = 200
PortionOfArtists = 20  # 10% to 30% (adjustable)
NumberOfProducers = int(PortionOfArtists * NumberOfUsers // 100)
EarliestJoinTime = datetime(2015, 1, 1)
LatestJoinTime = datetime(2023, 1, 1)

# Records
NumberOfReleases = 1000
PortionOfMovies = 30  # 1% to 50% of records are singles
NumberOfMovies = int(PortionOfMovies * NumberOfReleases // 100)
NumberOfSeries = NumberOfReleases - NumberOfMovies
ReleaseEarliestStartDate = datetime(2020, 1, 1)
ReleaseLatestEndDate = datetime(2024, 1, 1)

# Songs
MinVideoDuration = 60  # 60 minutes # normal distri
MaxVideoDuration = 600  # 600 minutes

# Sessions
NumberOfSessions = 5000
EarliestSessionStartTime = datetime(2023, 1, 2)

# Reviews


# Review Likes
# 0 - 500 per record

def generate_unique_id(prefix: str) -> str:
    """Generate a short unique ID with a given prefix."""
    short_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode('utf-8').rstrip("=")[:12]
    return f"{prefix}_{short_uuid}"