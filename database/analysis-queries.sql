-- 1. List all indexes in the database
SELECT
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;

-- 2. Get table sizes and estimated row counts
SELECT
    relname as table_name,
    pg_size_pretty(pg_total_relation_size(relid)) as total_size,
    pg_size_pretty(pg_relation_size(relid)) as table_size,
    pg_size_pretty(pg_total_relation_size(relid) - pg_relation_size(relid)) as index_size,
    n_live_tup as row_count
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

-- 3. Analyze specific table statistics
-- For Playlists
SELECT 
    COUNT(*) as total_playlists,
    AVG(num_followers) as avg_followers,
    MAX(num_followers) as max_followers,
    MIN(num_followers) as min_followers,
    AVG(num_tracks) as avg_tracks
FROM Playlists;

-- For Tracks
SELECT 
    COUNT(*) as total_tracks,
    COUNT(DISTINCT artist_name) as unique_artists,
    COUNT(DISTINCT album_name) as unique_albums
FROM Tracks;

-- For PlaylistTracks
SELECT 
    COUNT(*) as total_playlist_track_relations,
    COUNT(DISTINCT playlist_id) as unique_playlists,
    COUNT(DISTINCT track_uri) as unique_tracks
FROM PlaylistTracks;

-- 4. Analyze distribution of followers (for partitioning strategy)
SELECT 
    CASE 
        WHEN num_followers BETWEEN 0 AND 99 THEN '0-99'
        WHEN num_followers BETWEEN 100 AND 999 THEN '100-999'
        ELSE '1000+'
    END as follower_range,
    COUNT(*) as playlist_count,
    AVG(num_tracks) as avg_tracks_per_playlist
FROM Playlists
GROUP BY 
    CASE 
        WHEN num_followers BETWEEN 0 AND 99 THEN '0-99'
        WHEN num_followers BETWEEN 100 AND 999 THEN '100-999'
        ELSE '1000+'
    END
ORDER BY follower_range;

-- 5. Analyze most common artists (for potential indexing strategies)
SELECT 
    artist_name,
    COUNT(*) as track_count
FROM Tracks
GROUP BY artist_name
ORDER BY track_count DESC
LIMIT 10;