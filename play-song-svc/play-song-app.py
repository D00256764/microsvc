from flask import Flask, request, jsonify, render_template, url_for
import requests
import os

app = Flask(__name__)

CATALOG_URL = os.environ.get('CATALOG_URL', 'http://catalog:5000')

@app.route('/play-song')
def play_song():
    '''
    Return the play song page
    '''
    username = request.cookies.get('username')
    # get the song id from the request
    song_id = request.args.get('song_id')


    # make a http request to the song catalog service to get the song details
    song = requests.get(f'{CATALOG_URL}/play-song/{song_id}?username={username}', timeout=5)

    # get the song details from the song catalog service 
    # handle json decode error
    try:
        song_details = song.json()
    except:
        song_details = song.text
        
    app.logger.info('Song details: %s', song_details)
    

    return render_template('play-song.html.j2', song=song_details)



if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)