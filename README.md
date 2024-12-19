# Database Systems (CSCI-GA.2433) Final Project
NYU, Fall 2024

## Project: Analyzing Music Trends Using Spotify's Million Playlist Dataset

### Student Information
- Name: Dam, Anh
- NYU ID: N13366096
- Course: Database Systems – CSCIGA2433001

### GitHub Repository
```bash
git clone https://github.com/anhdamm/dam_final-project_fa24.git
cd dam_final-project_fa24
```

### Repository Structure
dam_final-project_fa24/
├── webapp/             # Flask application with ML integration
│   ├── static/         # CSS and JavaScript files
│   ├── templates/      # HTML templates
│   └── README.md       # Technical setup instructions
|
├── database/           # Database related files
|
├── ml_models/          # Machine learning models 
|
├── AnhDam_FinalProject_Report # Complete project report
└── README.md          # This file


### Setup Instructions

#### Prerequisites
- Python 3.8+
- PostgreSQL 13.0+
- pip (Python package manager)
- Spotify Million Playlist Dataset (Download from: https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge/dataset_files) (choose the spotify_million_playlist_dataset.zip)

#### Step 1: Database Setup and Data Loading
1. Create PostgreSQL database:
createdb spotify_playlist_db

2. Run SQL setup scripts:
# Connect to database
psql spotify_playlist_db

# Create tables and indexes
\i database/create_tables.sql

# Add Phase 2 updates
\i database/phase2_update.sql

# Populate artist table
\i database/populate_artist_table.sql

3. Load the dataset:
cd ml_models
python data_loading.py

This script will:
- Create necessary database tables
- Process the Spotify Million Playlist Dataset
- Load data into PostgreSQL tables

#### Step 2: Train Machine Learning Models
1. Train the playlist popularity predictor:
cd ml_models/playlist_predictor
python train_models.py

2. Train the artist clustering model:
cd ml_models/artist_clustering
python train_models.py

#### Step 3: Run the Web Application (go to webapp/README.md for more instruction)
1. Navigate to webapp directory:
cd webapp

2. Install requirements:
pip install -r requirements.txt

3. Start the Flask application:
python3 app.py

4. Access the application:
- Open your browser
- Navigate to http://127.0.0.1:8080
- Use the interface to analyze playlists and view artist clusters

### Documentation
Complete project documentation can be found in `/AnhDam_FinalProject_Report.pdf`

### Contact
- Email: adt9472@nyu.edu
- Course: Database Systems – CSCIGA2433001
- Semester: Fall 2024

### License
This project is submitted as part of the Database Systems course at NYU. All rights reserved.