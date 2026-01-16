
# Import the Flask and Redis classes
import json
from flask import Flask, request, jsonify, url_for
import os
import redis
import uuid
import time

REDIS_HOST = os.environ.get('REDIS_HOST', 'catalog-db')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', '')
SERVICE_PORT = os.environ.get('SERVICE_PORT', 5000)

# Create a Flask instance and connect to Redis
app = Flask(__name__)
def connect_to_redis():
    while True:
        try:
            r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0)
            r.ping()
            return r
        except redis.ConnectionError as e:
            app.logger.error('Failed to connect to Redis. Error: %s', e)
            time.sleep(5)

r = connect_to_redis()       

catalog = {'catalog': 
    {"Desert Rose-Ava Huang":{"name":"Desert Rose","artist":"Ava Huang","album":"Highs and Lows","year":"2012"},
    "Candy-Doja":{"name":"Candy","artist":"Doja Cat","album":"Amala","year":"2020"}}
    }

@app.route('/get-catalog')
def get_catalog():
    '''
    Return the catalog as json
    '''
    username = request.args.get('username', 'default_user')
    # get all keys and values from redis
    try:
        data = r.hgetall(f'catalog:{username}')
        data_str = {key.decode('utf-8'): json.loads(value.decode('utf-8')) for key, value in data.items()}
        return json.dumps({'catalog': data_str})
    except redis.RedisError as e:
        app.logger.error(f"Redis error: {e}")
        return jsonify({'error': 'An error occurred while fetching the catalog'})
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({'error': 'Unexpected error'})
        
    
    
# route to add a song to the catalog
@app.route('/upload-song', methods=['POST'])
def upload_song():
    '''
    Add a song to the catalog
    '''
    username = request.json.get('username', 'default_user') 
    song = {
        "name": request.json['name'],
        "artist": request.json['artist'],
        "genre": request.json['genre'],
        "album": request.json['album'],
        "year": request.json['year'],
        "filename": request.json['filename'],
        "location": request.json['location']
        }
    app.logger.info('Song details: %s', song)
    # get the song id created in the upload-song-svc
    key = request.json['song_id']

    # store key and value in redis. Convert json to string first
    r.hset(f'catalog:{username}', key=key, value=json.dumps(song))
    
    
    return 'Song added to catalog!'

# route to return song details for a given song id
@app.route('/play-song/<song_id>', methods=['GET'])
def play_song(song_id):
    '''
    Return the song details for a given song id
    '''
    username = request.args.get('username', 'default_user')
    # get the song details from redis
    song = r.hget(f'catalog:{username}', song_id)
    app.logger.info('Song details: %s', song)

    if song is None:
        return jsonify({'error': 'Song not found in your catalog'}), 404
    
    # convert stored string back to json,  keys must be str, int, float, bool or None, not bytes
    song_details = json.loads(song.decode('utf-8'))
    return jsonify(song_details)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)