-- Add new columns to Playlists table
ALTER TABLE Playlists 
ADD COLUMN IF NOT EXISTS predicted_followers INT,
ADD COLUMN IF NOT EXISTS last_processed TIMESTAMP WITH TIME ZONE;

-- Create Artists table for Phase 2
CREATE TABLE IF NOT EXISTS Artists (
    artist_name TEXT PRIMARY KEY,
    cluster_id INT,
    last_processed TIMESTAMP WITH TIME ZONE,
    playlist_count INT,
    avg_followers FLOAT,
    track_count INT
);

-- Create new indexes for Phase 2
CREATE INDEX IF NOT EXISTS idx_playlist_processed ON Playlists(last_processed);
CREATE INDEX IF NOT EXISTS idx_artist_cluster ON Artists(cluster_id);
CREATE INDEX IF NOT EXISTS idx_artist_processed ON Artists(last_processed);