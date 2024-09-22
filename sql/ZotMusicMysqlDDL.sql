DROP SCHEMA IF EXISTS ZotMusicMysql;
CREATE SCHEMA ZotMusicMysql;
USE ZotMusicMysql;

CREATE TABLE Users (
    user_id        VARCHAR(255) NOT NULL,  -- Changed from text to VARCHAR(255)
    email          VARCHAR(255) NOT NULL,  -- Changed from text to VARCHAR(255)
    joined_date    DATE NOT NULL,
    nickname       VARCHAR(255) NOT NULL,  -- Changed from text to VARCHAR(255)
    street         VARCHAR(255),
    city           VARCHAR(255),
    state          VARCHAR(255),
    zip            VARCHAR(10),
    PRIMARY KEY (user_id)
);

CREATE TABLE Artists (
    user_id        VARCHAR(255),  -- Changed from text to VARCHAR(255)
    bio            TEXT,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE
);

CREATE TABLE Listeners (
    user_id        VARCHAR(255),  -- Changed from text to VARCHAR(255)
    subscription   VARCHAR(50),   -- Changed from text to VARCHAR(50)
    first_name     VARCHAR(255) NOT NULL,  -- Changed from text to VARCHAR(255)
    last_name      VARCHAR(255) NOT NULL,  -- Changed from text to VARCHAR(255)
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE,
    CHECK (subscription IN ('free', 'monthly', 'yearly'))
);

CREATE TABLE Records (
    record_id      VARCHAR(255) NOT NULL,  -- Changed from text to VARCHAR(255)
    artist_user_id VARCHAR(255) NOT NULL,  -- Changed from text to VARCHAR(255)
    title          VARCHAR(255) NOT NULL,  -- Changed from text to VARCHAR(255)
    release_date   DATE,
    PRIMARY KEY (record_id),
    FOREIGN KEY (artist_user_id) REFERENCES Artists (user_id) ON DELETE CASCADE
);

CREATE TABLE Singles (
    record_id      VARCHAR(255) NOT NULL,  -- Changed from text to VARCHAR(255)
    video_url      TEXT NOT NULL,
    PRIMARY KEY (record_id),
    FOREIGN KEY (record_id) REFERENCES Records (record_id) ON DELETE CASCADE
);

CREATE TABLE Albums (
    record_id      VARCHAR(255) NOT NULL,  -- Changed from text to VARCHAR(255)
    description    TEXT,
    PRIMARY KEY (record_id),
    FOREIGN KEY (record_id) REFERENCES Records (record_id) ON DELETE CASCADE
);

CREATE TABLE Songs (
    record_id      VARCHAR(255) NOT NULL,  -- Changed from text to VARCHAR(255)
    track_number   INT NOT NULL,
    title          VARCHAR(255) NOT NULL,  -- Changed from text to VARCHAR(255)
    length         INT NOT NULL,  -- Song length in seconds
    bpm            INT,
    mood           VARCHAR(255) NOT NULL,  -- Changed from text to VARCHAR(255)
    PRIMARY KEY (record_id, track_number),
    FOREIGN KEY (record_id) REFERENCES Records (record_id) ON DELETE CASCADE
);

CREATE TABLE Sessions (
    session_id        VARCHAR(255) NOT NULL,  -- Changed from text to VARCHAR(255)
    user_id           VARCHAR(255) NOT NULL,  -- Changed from text to VARCHAR(255)
    record_id         VARCHAR(255) NOT NULL,  -- Changed from text to VARCHAR(255)
    track_number      INT NOT NULL,
    initiateAt        TIMESTAMP NOT NULL,
    leaveAt           TIMESTAMP NOT NULL,
    musicQuality      VARCHAR(255) NOT NULL,  -- Changed from text to VARCHAR(255)
    device            VARCHAR(255) NOT NULL,  -- Changed from text to VARCHAR(255)
    end_play_time     INT NOT NULL,
    replay_count      INT,
    PRIMARY KEY (session_id),
    FOREIGN KEY (user_id) REFERENCES Listeners(user_id) ON DELETE CASCADE,
    FOREIGN KEY (record_id, track_number) REFERENCES Songs(record_id, track_number) ON DELETE CASCADE
);

CREATE TABLE Reviews (
    review_id     VARCHAR(255) NOT NULL,  -- Changed from text to VARCHAR(255)
    user_id       VARCHAR(255) NOT NULL,  -- Changed from text to VARCHAR(255)
    record_id     VARCHAR(255) NOT NULL,  -- Changed from text to VARCHAR(255)
    rating        INT NOT NULL,
    body          TEXT,
    posted_at     TIMESTAMP NOT NULL,
    PRIMARY KEY (review_id),
    FOREIGN KEY (user_id) REFERENCES Listeners (user_id) ON DELETE CASCADE,
    FOREIGN KEY (record_id) REFERENCES Records (record_id) ON DELETE CASCADE
);

CREATE TABLE ReviewLikes (
    user_id   VARCHAR(255) NOT NULL,  -- Changed from text to VARCHAR(255)
    review_id VARCHAR(255) NOT NULL,  -- Changed from text to VARCHAR(255)
    PRIMARY KEY (user_id, review_id),
    FOREIGN KEY (user_id) REFERENCES Listeners(user_id) ON DELETE CASCADE,
    FOREIGN KEY (review_id) REFERENCES Reviews(review_id) ON DELETE CASCADE
);

-- Create the Genres table
CREATE TABLE Genres (
    genre_id   INT PRIMARY KEY,
    genre_name VARCHAR(255) NOT NULL  -- Changed from text to VARCHAR(255)
);

-- Create association table for Users and Genres
CREATE TABLE UserGenres (
    user_id  VARCHAR(255) NOT NULL,   -- Changed from text to VARCHAR(255)
    genre_id INT NOT NULL,
    PRIMARY KEY (user_id, genre_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES Genres(genre_id) ON DELETE CASCADE
);

-- Create association table for Records and Genres
CREATE TABLE RecordGenres (
    record_id VARCHAR(255) NOT NULL,  -- Changed from text to VARCHAR(255)
    genre_id  INT NOT NULL,
    PRIMARY KEY (record_id, genre_id),
    FOREIGN KEY (record_id) REFERENCES Records(record_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES Genres(genre_id) ON DELETE CASCADE
);
