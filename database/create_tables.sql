-- Create Playlists Table
CREATE TABLE IF NOT EXISTS Playlists (
    playlist_id INT PRIMARY KEY,
    name TEXT,
    description TEXT,
    modified_at TIMESTAMP,
    num_artists INT,
    num_albums INT,
    num_tracks INT,
    num_followers INT,
    num_edits INT,
    duration_ms BIGINT,
    collaborative BOOLEAN,
    -- Phase 2 additions
    predicted_followers INT,
    last_processed TIMESTAMP
);

-- Create Tracks Table
CREATE TABLE IF NOT EXISTS Tracks (
    track_id SERIAL PRIMARY KEY,
    track_uri TEXT UNIQUE,
    track_name TEXT,
    artist_name TEXT,
    artist_uri TEXT,
    album_name TEXT,
    album_uri TEXT,
    duration_ms BIGINT
);

-- Create PlaylistTracks Table
CREATE TABLE IF NOT EXISTS PlaylistTracks (
    playlist_id INT,
    track_uri TEXT,
    position INT,
    PRIMARY KEY (playlist_id, track_uri),
    FOREIGN KEY (playlist_id) REFERENCES Playlists(playlist_id) ON DELETE CASCADE,
    FOREIGN KEY (track_uri) REFERENCES Tracks(track_uri) ON DELETE CASCADE
);

-- New Artists Table for Phase 2
CREATE TABLE IF NOT EXISTS Artists (
    artist_name TEXT PRIMARY KEY,
    cluster_id INT,
    last_processed TIMESTAMP,
    playlist_count INT,
    avg_followers FLOAT,
    track_count INT
);

-- Create indexes (with IF NOT EXISTS)
CREATE INDEX IF NOT EXISTS idx_playlist_modified ON Playlists(modified_at);
CREATE INDEX IF NOT EXISTS idx_playlist_followers ON Playlists(num_followers);
CREATE INDEX IF NOT EXISTS idx_playlist_name ON Playlists(name);
CREATE INDEX IF NOT EXISTS idx_playlist_processed ON Playlists(last_processed);

CREATE INDEX IF NOT EXISTS idx_track_artist ON Tracks(artist_name);
CREATE INDEX IF NOT EXISTS idx_track_name ON Tracks(track_name);
CREATE INDEX IF NOT EXISTS idx_track_uri ON Tracks(track_uri);
CREATE INDEX IF NOT EXISTS idx_album_name ON Tracks(album_name);

CREATE INDEX IF NOT EXISTS idx_playlisttracks_track ON PlaylistTracks(track_uri);
CREATE INDEX IF NOT EXISTS idx_playlisttracks_playlist ON PlaylistTracks(playlist_id);

CREATE INDEX IF NOT EXISTS idx_artist_cluster ON Artists(cluster_id);
CREATE INDEX IF NOT EXISTS idx_artist_processed ON Artists(last_processed);

CREATE INDEX IF NOT EXISTS idx_track_artist_name ON Tracks(artist_name, track_name);