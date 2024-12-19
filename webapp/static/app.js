async function analyzePlaylist() {
    const resultsDiv = document.getElementById('playlist-results');
    resultsDiv.innerHTML = 'Analyzing playlists...';
    
    try {
        const response = await fetch('/analyze_playlist', {
            method: 'POST'
        });
        const data = await response.json();
        
        if (data.status === 'success') {
            resultsDiv.innerHTML = `
                <h3>Results:</h3>
                <p>RMSE: ${data.rmse.toFixed(2)}</p>
                <p>R² Score: ${data.r2.toFixed(2)}</p>
                <h4>Top Features:</h4>
                <ul>
                    ${Object.entries(data.feature_importance)
                        .sort(([,a],[,b]) => b-a)
                        .slice(0,5)
                        .map(([feature, importance]) => 
                            `<li>${feature}: ${importance.toFixed(4)}</li>`
                        ).join('')}
                </ul>
            `;
        } else {
            resultsDiv.innerHTML = `Error: ${data.message}`;
        }
    } catch (error) {
        resultsDiv.innerHTML = `Error: ${error.message}`;
    }
}

async function analyzeArtists() {
    const resultsDiv = document.getElementById('artist-results');
    resultsDiv.innerHTML = 'Analyzing artists...';
    
    try {
        const response = await fetch('/analyze_artists', {
            method: 'POST'
        });
        const data = await response.json();
        
        if (data.status === 'success') {
            resultsDiv.innerHTML = `
                <h3>Cluster Sizes:</h3>
                <ul>
                    ${Object.entries(data.clusters)
                        .map(([cluster, size]) => 
                            `<li>Cluster ${cluster}: ${size} artists</li>`
                        ).join('')}
                </ul>
            `;
        } else {
            resultsDiv.innerHTML = `Error: ${data.message}`;
        }
    } catch (error) {
        resultsDiv.innerHTML = `Error: ${error.message}`;
    }
}