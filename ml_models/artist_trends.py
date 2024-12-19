import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
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
    filename=os.path.join(log_dir, 'artist_trends.log'),
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ArtistTrendAnalyzer:
    def __init__(self, db_params=None):
        """Initialize the analyzer with database connection and model"""
        logger.info("Initializing ArtistTrendAnalyzer")
        self.model = KMeans(
            n_clusters=5,
            random_state=42,
            n_init=10
        )
        # Create SQLAlchemy engine
        self.engine = create_engine('postgresql://postgres:1111@localhost/spotify_million')
        self.scaler = StandardScaler()
        logger.info("Initialization complete")

    def load_data(self):
        """Load artist data from database"""
        logger.info("Loading artist data")
        query = """
        SELECT 
            t.artist_name,
            COUNT(DISTINCT pt.playlist_id) as playlist_count,
            AVG(p.num_followers) as avg_followers,
            COUNT(DISTINCT t.track_uri) as track_count
        FROM Tracks t
        JOIN PlaylistTracks pt ON t.track_uri = pt.track_uri
        JOIN Playlists p ON pt.playlist_id = p.playlist_id
        GROUP BY t.artist_name
        HAVING COUNT(DISTINCT pt.playlist_id) > 10
        """
        
        try:
            df = pd.read_sql(query, self.engine)
            logger.info(f"Loaded data for {len(df)} artists")
            return df
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def prepare_features(self, df):
        """Prepare and scale features for clustering"""
        logger.info("Preparing features")
        try:
            # Create feature matrix
            features = pd.DataFrame()
            
            # Basic features
            features['playlist_count'] = df['playlist_count']
            features['avg_followers'] = df['avg_followers']
            features['track_count'] = df['track_count']
            
            # Derived features
            features['followers_per_playlist'] = df['avg_followers'] / df['playlist_count'].clip(lower=1)
            features['tracks_per_playlist'] = df['track_count'] / df['playlist_count'].clip(lower=1)
            
            # Scale features
            scaled_features = self.scaler.fit_transform(features)
            scaled_df = pd.DataFrame(
                scaled_features,
                columns=features.columns,
                index=features.index
            )
            
            logger.info("Feature preparation complete")
            return scaled_df
        except Exception as e:
            logger.error(f"Error preparing features: {str(e)}")
            raise

    def plot_clusters(self, df, clusters):
        """Create visualization of artist clusters"""
        logger.info("Creating cluster visualization")
        try:
            plt.switch_backend('Agg')
            plt.figure(figsize=(12, 8))
            
            scatter = plt.scatter(
                df['playlist_count'],
                df['avg_followers'],
                c=clusters,
                cmap='viridis',
                alpha=0.6
            )
            
            plt.xlabel('Number of Playlist Appearances')
            plt.ylabel('Average Followers')
            plt.title('Artist Clusters')
            plt.colorbar(scatter, label='Cluster')
            plt.grid(True, alpha=0.3)
            
            # Format axes for better readability
            plt.ticklabel_format(style='plain', axis='both')
            
            plot_path = os.path.join(log_dir, 'artist_clusters.png')
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Cluster visualization saved to {plot_path}")
        except Exception as e:
            logger.error(f"Error creating cluster visualization: {str(e)}")
            logger.error("Continuing without plot generation")

    def analyze(self):
        """Perform clustering analysis and return results"""
        logger.info("Starting artist trend analysis")
        try:
            # Load and prepare data
            df = self.load_data()
            scaled_features = self.prepare_features(df)
            
            # Perform clustering
            logger.info("Performing KMeans clustering...")
            clusters = self.model.fit_predict(scaled_features)
            
            # Add clusters to original dataframe
            df['cluster'] = clusters
            
            # Try to create visualization
            try:
                self.plot_clusters(df, clusters)
            except Exception as e:
                logger.warning(f"Could not create cluster visualization: {str(e)}")
            
            # Calculate cluster statistics
            stats = {}
            for cluster in range(self.model.n_clusters):
                cluster_data = df[df['cluster'] == cluster]
                stats[str(cluster)] = {
                    'size': len(cluster_data),
                    'avg_playlist_count': float(cluster_data['playlist_count'].mean()),
                    'avg_followers': float(cluster_data['avg_followers'].mean()),
                    'avg_track_count': float(cluster_data['track_count'].mean()),
                    'min_followers': float(cluster_data['avg_followers'].min()),
                    'max_followers': float(cluster_data['avg_followers'].max())
                }
            
            # Prepare results
            results = {
                'cluster_sizes': df['cluster'].value_counts().to_dict(),
                'cluster_stats': stats
            }
            
            logger.info("Analysis completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Error in analysis process: {str(e)}")
            raise

def main():
    """Test the analyzer independently"""
    try:
        analyzer = ArtistTrendAnalyzer()
        results = analyzer.analyze()
        print("\nClustering Results:")
        print(f"Number of clusters: {results['n_clusters']}")
        print(f"Inertia: {results['inertia']:.2f}")
        print("\nCluster sizes:")
        for cluster, size in results['cluster_sizes'].items():
            print(f"Cluster {cluster}: {size} artists")
    except Exception as e:
        print(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()