-- Populate Artists table from existing data
INSERT INTO Artists (
    artist_name,
    playlist_count,
    avg_followers,
    track_count,
    last_processed
)
SELECT 
    t.artist_name,
    COUNT(DISTINCT pt.playlist_id) as playlist_count,
    AVG(p.num_followers) as avg_followers,
    COUNT(DISTINCT t.track_uri) as track_count,
    NULL as last_processed  -- Will be updated when processed by ML
FROM Tracks t
JOIN PlaylistTracks pt ON t.track_uri = pt.track_uri
JOIN Playlists p ON pt.playlist_id = p.playlist_id
GROUP BY t.artist_name
HAVING COUNT(DISTINCT pt.playlist_id) > 10;