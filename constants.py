from datetime import datetime
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

# Songs
NumberOfSongs = 2000
MinSongDuration = 120  # 2 minutes
MaxSongDuration = 360  # 6 minutes

# Sessions
NumberOfSessions = 3000
MinSessionDuration = 120  # 2 minutes
MaxSessionDuration = 360  # 6 minutes

# Reviews
NumberOfReviews = 1000
MinRating = 1
MaxRating = 5

# Review Likes
NumberOfReviewLikes = 5000
MinLikesPerReview = 0
MaxLikesPerReview = 50

# Record Descriptions
MinDescriptionLength = 100
MaxDescriptionLength = 500
