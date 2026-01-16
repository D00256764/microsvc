from flask import Flask, render_template, request, url_for, jsonify
import requests
import os
app = Flask(__name__)

CATALOG_URL = os.environ.get('CATALOG_URL', 'http://catalog:5000')

@app.route('/get-catalog', methods=['GET','POST'])
def get_catalog():
    '''
    Get the list of songs from the catalog service and be able to search for a song
    '''
    username = request.cookies.get('username')
    catalog = requests.get(f"{CATALOG_URL}/get-catalog?username={username}", timeout=5)
    songs = catalog.json()
    if request.method == 'POST':
        try:
            search = request.form['search']
            search_results = [(song_id, song) for song_id, song in songs['catalog'].items() if search.lower() in song['name'].lower()]
            return render_template('list-search.html.j2', catalog=dict(search_results))
    
        except Exception as e:
            app.logger.error(f"An error occurred: {e}")
            return jsonify({'error': 'Unexpected error'})
        
    return render_template('list-search.html.j2', catalog=songs['catalog'])

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port=5000)