# Spotify Million Playlist Analysis Web Application

## Overview
This web application provides an interface for analyzing the Spotify Million Playlist Dataset using machine learning models. It visualizes playlist popularity predictions and artist clustering results.

## Features
1. **Playlist Popularity Analysis**
   - Predicts playlist popularity using Random Forest
   - Shows feature importance visualization
   - Displays RMSE and R² metrics

2. **Artist Trend Analysis**
   - Clusters artists based on popularity patterns
   - Provides statistical summaries
   - Shows cluster visualization

## Setup and Running

### Prerequisites
- Python 3.8+
- PostgreSQL 13+
- pip (Python package installer)

### Database Configuration
Update database credentials in `config.py`:
```python
DB_PARAMS = {
    'host': 'localhost',
    'database': 'spotify_playlist_db',
    'user': 'your_username',
    'password': 'your_password',
    'port': '5432'
}
```

### Running the Application
1. Navigate to webapp directory:
```bash
cd webapp
```

2. Create and activate virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the application:
```bash
python3 app.py
```

5. Access the application:
- Open browser
- Go to: http://localhost:8080
- Use the "Run Analysis" buttons to execute models

## Technical Details

### Application Structure
- Flask web server
- PostgreSQL database integration
- Scikit-learn ML models
- D3.js visualizations

### API Endpoints
1. Playlist Analysis
   - POST /analyze_playlist
   - Shows prediction results and feature importance

2. Artist Analysis
   - POST /analyze_artist
   - Displays clustering results and statistics

## Troubleshooting

### Common Issues
1. Database Connection
   - Verify PostgreSQL is running
   - Check credentials in config
   - Default port is 5432

2. Application Access
   - Ensure port 8080 is available
   - Check terminal for errors
   - Verify requirements are installed

For complete project setup including database initialization and model training, please refer to the main README.md in the root directory.