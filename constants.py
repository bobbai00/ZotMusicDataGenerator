from datetime import datetime

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
MUSIC_QUALITY_OPTIONS = ['disaster', 'poor', 'normal', 'good', 'great']
DEVICE_OPTIONS = ['mobile', 'laptop', 'desktop', 'tablet', 'smart speaker']

Seed = 1234

# Users
NumberOfUsers = 200
PortionOfArtists = 20  # 10% to 30% (adjustable)
NumberOfArtists = int(PortionOfArtists * NumberOfUsers // 100)
NumberOfListeners = NumberOfUsers - NumberOfArtists
EarliestJoinTime = datetime(2015, 1, 1)
LatestJoinTime = datetime(2023, 1, 1)

# Records
NumberOfRecords = 500
PortionOfSingles = 30  # 1% to 50% of records are singles
NumberOfSingles = int(PortionOfSingles * NumberOfRecords // 100)
NumberOfAlbums = NumberOfRecords - NumberOfSingles
RecordEarliestStartDate =  datetime(1980, 1, 1)
RecordLatestEndDate = datetime(2023, 1, 1)

# Songs
MinSongDuration = 120  # 2 minutes
MaxSongDuration = 360  # 6 minutes

# Sessions
NumberOfSessions = 1000
EarliestSessionStartTime = datetime(2023, 1, 2)

# Reviews
NumberOfReviews = 1000
MinRating = 1
MaxRating = 5

# Review Likes
NumberOfReviewLikes = 1000
MinLikesPerReview = 0
MaxLikesPerReview = 50
