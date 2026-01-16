# Allow any user to upload a song

from flask import Flask, request, render_template, jsonify, url_for, redirect
from fileinput import filename
import requests 
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)

storage_dir = '/usr/share/nginx/html/songs/'

# ensure the storage directory exists
os.makedirs(storage_dir, exist_ok=True)

CATALOG_URL = os.environ.get('CATALOG_URL', 'http://catalog:5000')


# router upload-song
@app.route('/upload-song', methods=['POST', 'GET'])
def upload_song():
    username = request.cookies.get('username')
    if request.method == 'POST':
        name=request.form['name']
        artist=request.form['artist']
        genre=request.form['genre']
        album=request.form['album']
        year=request.form['year']
        
        song_id = str(uuid.uuid4())

        file = request.files['file']
        filename = secure_filename(file.filename)
        file_path = os.path.join(storage_dir, filename)
        file.save(file_path)

        song = {
            'username': username,
            'song_id': song_id, 
            'name': name, 
            'artist': artist, 
            'genre': genre, 
            'album': album, 
            'year': year,
            'filename': filename,
            'location': file_path
        }

        requests.post(f'{CATALOG_URL}/upload-song', json=song, timeout=5)
        return redirect('/get-catalog')
    
    return render_template("upload-song.html.j2")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)