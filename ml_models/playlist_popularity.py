import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sqlalchemy import create_engine
import logging
from datetime import datetime, timezone
import os

# Configure matplotlib for non-interactive backend
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Setup logging
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    filename=os.path.join(log_dir, 'playlist_popularity.log'),
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PlaylistPopularityPredictor:
    def __init__(self, db_params=None):
        """Initialize the predictor with database connection and model"""
        logger.info("Initializing PlaylistPopularityPredictor")
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        # Create SQLAlchemy engine
        self.engine = create_engine('postgresql://postgres:1111@localhost/spotify_million')
        logger.info("Initialization complete")

    def load_training_data(self):
        """Load and prepare training data from database"""
        logger.info("Loading training data")
        query = """
        SELECT 
            p.playlist_id,
            p.num_tracks,
            p.num_artists,
            p.num_albums,
            p.duration_ms,
            p.collaborative,
            p.num_followers as actual_followers,
            COUNT(DISTINCT t.artist_name) as unique_artists,
            AVG(t.duration_ms) as avg_track_duration
        FROM Playlists p
        JOIN PlaylistTracks pt ON p.playlist_id = pt.playlist_id
        JOIN Tracks t ON pt.track_uri = t.track_uri
        GROUP BY p.playlist_id
        """
        
        try:
            df = pd.read_sql(query, self.engine)
            logger.info(f"Loaded {len(df)} playlists for training")
            return df
        except Exception as e:
            logger.error(f"Error loading training data: {str(e)}")
            raise

    def prepare_features(self, df):
        """Prepare features for training"""
        logger.info("Preparing features")
        try:
            # Create a new DataFrame for features
            features = pd.DataFrame()
            
            # Add basic features
            features['num_tracks'] = df['num_tracks']
            features['num_artists'] = df['num_artists']
            features['num_albums'] = df['num_albums']
            features['duration_ms'] = df['duration_ms']
            features['unique_artists'] = df['unique_artists']
            features['avg_track_duration'] = df['avg_track_duration']
            features['collaborative'] = df['collaborative'].astype(int)
            
            # Add derived features
            features['tracks_per_artist'] = df['num_tracks'] / df['num_artists'].clip(lower=1)
            features['avg_tracks_per_album'] = df['num_tracks'] / df['num_albums'].clip(lower=1)
            
            logger.info("Feature preparation complete")
            return features
        except Exception as e:
            logger.error(f"Error preparing features: {str(e)}")
            raise

    def plot_feature_importance(self, feature_names):
        """Plot feature importance"""
        logger.info("Creating feature importance plot")
        try:
            importance = self.model.feature_importances_
            indices = np.argsort(importance)[::-1]
            
            plt.switch_backend('Agg')
            plt.figure(figsize=(10, 6))
            plt.title('Feature Importance for Playlist Popularity')
            plt.bar(range(len(importance)), importance[indices])
            plt.xticks(range(len(importance)), [feature_names[i] for i in indices], rotation=45)
            plt.tight_layout()
            
            plot_path = os.path.join(log_dir, 'feature_importance.png')
            plt.savefig(plot_path)
            plt.close()
            
            logger.info(f"Feature importance plot saved to {plot_path}")
        except Exception as e:
            logger.error(f"Error creating feature importance plot: {str(e)}")
            logger.error("Continuing without plot generation")

    def train(self):
        """Train the model and return results"""
        logger.info("Starting model training")
        try:
            # Load and prepare data
            df = self.load_training_data()
            features = self.prepare_features(df)
            target = df['actual_followers']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                features, target, test_size=0.2, random_state=42
            )
            
            # Train model
            logger.info("Training Random Forest model...")
            self.model.fit(X_train, y_train)
            
            # Make predictions
            predictions = self.model.predict(X_test)
            
            # Calculate metrics
            rmse = np.sqrt(mean_squared_error(y_test, predictions))
            r2 = r2_score(y_test, predictions)
            
            logger.info(f"Model Performance - RMSE: {rmse:.2f}, R2: {r2:.2f}")
            
            # Generate feature importance data
            feature_importance = dict(zip(features.columns, self.model.feature_importances_))
            
            # Try to create plot, but don't fail if it errors
            try:
                self.plot_feature_importance(features.columns)
            except Exception as e:
                logger.warning(f"Could not create feature importance plot: {str(e)}")
            
            return {
                'rmse': float(rmse),
                'r2': float(r2),
                'feature_importance': feature_importance
            }
            
        except Exception as e:
            logger.error(f"Error in training process: {str(e)}")
            raise

def main():
    """Test the model independently"""
    try:
        predictor = PlaylistPopularityPredictor()
        results = predictor.train()
        print("\nModel Results:")
        print(f"RMSE: {results['rmse']:.2f}")
        print(f"R2 Score: {results['r2']:.2f}")
        print("\nTop Feature Importance:")
        for feature, importance in sorted(
            results['feature_importance'].items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]:
            print(f"{feature}: {importance:.4f}")
    except Exception as e:
        print(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()