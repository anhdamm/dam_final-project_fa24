import os
import json
import psycopg2
from datetime import datetime
from tqdm import tqdm
import logging

class SpotifyDataLoader:
    def __init__(self, db_params, data_dir="../data"):
        self.db_params = db_params
        self.data_dir = data_dir
        self.setup_logging()
        self.processed_count = 0
        self.start_time = datetime.now()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='spotify_data_loading.log',
            filemode='a'
        )
        # Also print to console
        console_handler = logging.StreamHandler()
        logging.getLogger().addHandler(console_handler)

    def connect_db(self):
        return psycopg2.connect(**self.db_params)

    def process_playlist(self, playlist, cur):
        try:
            # Insert playlist
            cur.execute("""
                INSERT INTO Playlists (playlist_id, name, description, modified_at,
                                     num_artists, num_albums, num_tracks, num_followers,
                                     num_edits, duration_ms, collaborative)
                VALUES (%s, %s, %s, to_timestamp(%s), %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (playlist_id) DO NOTHING
            """, (
                playlist['pid'], 
                playlist['name'],
                playlist.get('description'),
                playlist['modified_at'],
                playlist['num_artists'],
                playlist['num_albums'],
                playlist['num_tracks'],
                playlist['num_followers'],
                playlist['num_edits'],
                playlist['duration_ms'],
                playlist['collaborative'] == 'true'
            ))

            # Insert tracks and playlist-track relationships
            for track in playlist['tracks']:
                # Insert track
                cur.execute("""
                    INSERT INTO Tracks (track_uri, track_name, artist_name, artist_uri,
                                      album_name, album_uri, duration_ms)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (track_uri) DO NOTHING
                """, (
                    track['track_uri'],
                    track['track_name'],
                    track['artist_name'],
                    track['artist_uri'],
                    track['album_name'],
                    track['album_uri'],
                    track['duration_ms']
                ))

                # Insert playlist-track relationship
                cur.execute("""
                    INSERT INTO PlaylistTracks (playlist_id, track_uri, position)
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, (playlist['pid'], track['track_uri'], track['pos']))

            return True
        except Exception as e:
            logging.error(f"Error processing playlist {playlist['pid']}: {str(e)}")
            return False

    def process_slice_file(self, filename):
        file_path = os.path.join(self.data_dir, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                slice_data = json.load(f)
                
            with self.connect_db() as conn:
                with conn.cursor() as cur:
                    for playlist in slice_data['playlists']:
                        try:
                            cur.execute("BEGIN")
                            if self.process_playlist(playlist, cur):
                                conn.commit()
                                self.processed_count += 1
                            else:
                                conn.rollback()
                        except Exception as e:
                            conn.rollback()
                            logging.error(f"Transaction error for playlist {playlist['pid']}: {str(e)}")

        except Exception as e:
            logging.error(f"Error processing file {filename}: {str(e)}")

    def load_data(self):
        logging.info("Starting data loading process")
        
        # Get list of slice files
        slice_files = [f for f in os.listdir(self.data_dir) if f.startswith('mpd.slice.') and f.endswith('.json')]
        total_files = len(slice_files)
        
        logging.info(f"Found {total_files} slice files to process")

        # Process each slice file with progress bar
        for filename in tqdm(slice_files, desc="Processing slice files"):
            self.process_slice_file(filename)
            
            # Log progress every 10 files
            if slice_files.index(filename) % 10 == 0:
                elapsed_time = datetime.now() - self.start_time
                avg_time_per_playlist = elapsed_time / max(self.processed_count, 1)
                estimated_remaining = avg_time_per_playlist * (1000000 - self.processed_count)
                
                logging.info(f"""
                    Progress Update:
                    Processed playlists: {self.processed_count}
                    Elapsed time: {elapsed_time}
                    Estimated time remaining: {estimated_remaining}
                """)

        end_time = datetime.now()
        total_time = end_time - self.start_time
        
        logging.info(f"""
            Data Loading Completed:
            Total playlists processed: {self.processed_count}
            Total processing time: {total_time}
        """)

def main():
    # Database connection parameters
    db_params = {
        "dbname": "spotify_million",
        "user": "postgres",
        "password": "1111",
        "host": "localhost",
        "port": "5432"
    }

    # Initialize and run loader
    loader = SpotifyDataLoader(db_params)
    loader.load_data()

if __name__ == "__main__":
    main()