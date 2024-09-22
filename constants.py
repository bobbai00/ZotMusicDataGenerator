from datetime import datetime

MySQLDBUrl = 'mysql+pymysql://root:123456@localhost'
DBName = 'ZotMusicMysql'

Seed = 1234

# Users
NumberOfUsers = 20
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
ApproximateNumberOfSongs = 2000
MinSongDuration = 120  # 2 minutes
MaxSongDuration = 360  # 6 minutes

# Sessions
NumberOfSessions = 3000
EarliestSessionStartTime = datetime(2023, 1, 2)

# Reviews
NumberOfReviews = 1000
MinRating = 1
MaxRating = 5

# Review Likes
NumberOfReviewLikes = 5000
MinLikesPerReview = 0
MaxLikesPerReview = 50
