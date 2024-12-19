from flask import Flask, render_template, jsonify, request, send_from_directory
import sys
import os
import logging

# Add parent directory to path to import ml_models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup logging
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ml_models/logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    filename=os.path.join(log_dir, 'webapp.log'),
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from ml_models.playlist_popularity import PlaylistPopularityPredictor
from ml_models.artist_trends import ArtistTrendAnalyzer

app = Flask(__name__)

@app.route('/')
def home():
    logger.info("Home page accessed")
    return render_template('index.html')

@app.route('/analyze_playlist', methods=['POST'])
def analyze_playlist():
    logger.info("Playlist analysis requested")
    try:
        predictor = PlaylistPopularityPredictor()
        results = predictor.train()
        logger.info(f"Playlist analysis completed successfully")
        return jsonify({
            'status': 'success',
            'rmse': results['rmse'],
            'r2': results['r2'],
            'feature_importance': results['feature_importance']
        })
    except Exception as e:
        logger.error(f"Error in playlist analysis: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/analyze_artists', methods=['POST'])
def analyze_artists():
    logger.info("Artist analysis requested")
    try:
        analyzer = ArtistTrendAnalyzer()
        results = analyzer.analyze()
        logger.info("Artist analysis completed successfully")
        return jsonify({
            'status': 'success',
            'clusters': results['cluster_sizes'],
            'cluster_stats': results['cluster_stats']
        })
    except Exception as e:
        logger.error(f"Error in artist analysis: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/plots/<path:filename>')
def serve_plot(filename):
    """Serve plot images"""
    plots_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ml_models/logs')
    return send_from_directory(plots_dir, filename)

if __name__ == '__main__':
    # Print startup messages
    print("Starting Flask application...")
    print(f"Server will be available at http://127.0.0.1:8080")
    print("Press CTRL+C to quit")
    
    # Log startup
    logger.info("Starting Flask application")
    logger.info("Server will be available at http://127.0.0.1:8080")
    
    # Run the app
    app.run(debug=True, host='127.0.0.1', port=8080)