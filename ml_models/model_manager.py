import logging
from datetime import datetime, timezone
import psycopg2
import pandas as pd
from playlist_popularity import PlaylistPopularityPredictor
from artist_trends import ArtistTrendAnalyzer

class ModelManager:
    def __init__(self, db_params):
        self.db_params = db_params
        self.setup_logging()
        self.pp_model = PlaylistPopularityPredictor()
        self.artist_model = ArtistTrendAnalyzer()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='logs/model_training.log',
            filemode='a'
        )
        console_handler = logging.StreamHandler()
        logging.getLogger().addHandler(console_handler)

    def needs_processing(self):
        """Check if there's enough new data to warrant reprocessing"""
        with psycopg2.connect(**self.db_params) as conn:
            with conn.cursor() as cur:
                # Check playlists needing prediction
                cur.execute("""
                    SELECT COUNT(*) FROM Playlists 
                    WHERE last_processed IS NULL 
                    OR last_processed < modified_at
                """)
                playlists_pending = cur.fetchone()[0]
                
                # Check artists needing clustering
                cur.execute("""
                    SELECT COUNT(*) FROM Artists 
                    WHERE last_processed IS NULL
                """)
                artists_pending = cur.fetchone()[0]
                
                return playlists_pending > 100 or artists_pending > 50

    def update_models(self):
        """Run the complete model update process"""
        try:
            logging.info("Starting model update process")
            
            # Train and update playlist predictions
            logging.info("Training playlist popularity model...")
            playlist_results = self.pp_model.train()
            
            # Train and update artist clusters
            logging.info("Training artist clustering model...")
            artist_results = self.artist_model.analyze()
            
            # Update database with results
            self.save_results(playlist_results, artist_results)
            
            logging.info("Model update process completed successfully")
            return True
            
        except Exception as e:
            logging.error(f"Error in model update process: {str(e)}")
            return False
    
    def save_results(self, playlist_results, artist_results):
        """Save model results to database"""
        current_time = datetime.now(timezone.utc)
        
        with psycopg2.connect(**self.db_params) as conn:
            with conn.cursor() as cur:
                # Update playlist predictions
                for pid, pred in playlist_results['predictions'].items():
                    cur.execute("""
                        UPDATE Playlists 
                        SET predicted_followers = %s,
                            last_processed = %s
                        WHERE playlist_id = %s
                    """, (pred, current_time, pid))
                
                # Update artist clusters
                for artist, cluster in artist_results['clusters'].items():
                    cur.execute("""
                        UPDATE Artists 
                        SET cluster_id = %s,
                            last_processed = %s
                        WHERE artist_name = %s
                    """, (cluster, current_time, artist))
                
                conn.commit()

def main():
    # Database connection parameters
    db_params = {
        "dbname": "spotify_million",
        "user": "postgres",
        "password": "1111",
        "host": "localhost",
        "port": "5432"
    }
    
    manager = ModelManager(db_params)
    if manager.needs_processing():
        manager.update_models()

if __name__ == "__main__":
    main()