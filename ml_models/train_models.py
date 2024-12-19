from playlist_popularity import PlaylistPopularityPredictor
from artist_trends import ArtistTrendAnalyzer
import logging
from datetime import datetime
import os

def setup_logging():
    """Setup logging configuration"""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='logs/model_testing.log',
        filemode='a'
    )
    # Also print to console
    console_handler = logging.StreamHandler()
    logging.getLogger().addHandler(console_handler)

def test_playlist_popularity():
    """Test the playlist popularity prediction model"""
    print("\n=== Testing Playlist Popularity Predictor ===")
    print("Training model and generating predictions...")
    
    try:
        predictor = PlaylistPopularityPredictor()
        results = predictor.train()
        
        print("\nModel Performance:")
        print(f"RMSE: {results['rmse']:.2f}")
        print(f"R2 Score: {results['r2']:.2f}")
        
        print("\nTop 5 Feature Importance:")
        sorted_features = sorted(
            results['feature_importance'].items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        for feature, importance in sorted_features:
            print(f"{feature}: {importance:.4f}")
            
        print("\nFeature importance plot saved as 'logs/feature_importance.png'")
        return True
        
    except Exception as e:
        logging.error(f"Error in playlist popularity testing: {str(e)}")
        print(f"Error: {str(e)}")
        return False

def test_artist_clustering():
    """Test the artist trend analysis and clustering"""
    print("\n=== Testing Artist Trend Analyzer ===")
    print("Performing clustering analysis...")
    
    try:
        analyzer = ArtistTrendAnalyzer()
        results = analyzer.analyze()
        
        print("\nClustering Results:")
        print(f"Number of clusters: {results['n_clusters']}")
        print(f"Inertia: {results['inertia']:.2f}")
        
        print("\nCluster Sizes:")
        for cluster, size in results['cluster_sizes'].items():
            print(f"Cluster {cluster}: {size} artists")
        
        print("\nSample Artists per Cluster:")
        for cluster_id in range(results['n_clusters']):
            artists = [
                artist for artist, c in results['clusters'].items() 
                if c == cluster_id
            ][:3]
            print(f"\nCluster {cluster_id} sample artists:")
            for artist in artists:
                print(f"  - {artist}")
        
        print("\nCluster Statistics:")
        stats = results['cluster_stats']
        for cluster in range(results['n_clusters']):
            print(f"\nCluster {cluster}:")
            print(f"  Average Playlist Count: {stats[('playlist_count', 'mean')][cluster]:.2f}")
            print(f"  Average Followers: {stats[('avg_followers', 'mean')][cluster]:.2f}")
            print(f"  Average Track Count: {stats[('track_count', 'mean')][cluster]:.2f}")
            
        print("\nClustering visualization saved as 'logs/artist_clusters.png'")
        return True
        
    except Exception as e:
        logging.error(f"Error in artist clustering testing: {str(e)}")
        print(f"Error: {str(e)}")
        return False

def main():
    """Main testing function"""
    print("=== Starting Model Testing ===")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    setup_logging()
    
    try:
        # Test playlist popularity prediction
        pp_success = test_playlist_popularity()
        
        # Test artist clustering
        artist_success = test_artist_clustering()
        
        # Summary
        print("\n=== Testing Summary ===")
        print(f"Playlist Popularity Model: {'SUCCESS' if pp_success else 'FAILED'}")
        print(f"Artist Trend Analysis: {'SUCCESS' if artist_success else 'FAILED'}")
        
        print("\nVisualizations saved in 'logs' directory:")
        print("- logs/feature_importance.png")
        print("- logs/artist_clusters.png")
        print("- logs/model_testing.log")
        
        if pp_success and artist_success:
            print("\nAll tests completed successfully!")
        else:
            print("\nSome tests failed. Check the log file for details.")
            
    except Exception as e:
        logging.error(f"Error during testing: {str(e)}")
        print(f"\nError during testing: {str(e)}")
        print("Check logs/model_testing.log for details")

if __name__ == "__main__":
    main()