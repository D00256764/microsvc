
from flask import Flask, render_template, request, redirect, url_for, make_response
import redis
import os
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
@app.route('/login', methods=['GET','POST'])
def login():
    message = request.args.get('message')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if r.exists(username):
            # If the username exists, check if the password matches
            if r.get(username).decode('utf-8') == password:
                #response = make_response(redirect('http://localhost/get-catalog'))
                response = make_response(redirect('/get-catalog'))
                response.set_cookie('username', username)
                return response
            else:
                return redirect(url_for('login', message="Invalid Credentials, Please try again!"))
        else:
            # If the username doesn't exist, redirect the user back to the login page with an error message
            return redirect(url_for('login', message="User isn't registered. Please sign up to continue."))

    return render_template("login.html.j2", message=message)


@app.route('/register', methods=['GET','POST'])
def register():
    message = request.args.get('message')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        
        #check if username already exists
        if r.exists(username):
            return render_template("register.html.j2", message="Username already exists. Please choose another username.")

        #check if password and confirm password match
        if password != confirm_password:
            return render_template("register.html.j2", message="Passwords do not match. Please try again.")
        
        r.set(username, password)
        return redirect(url_for('login', message="Registration Successful! Please login to continue to app."))
    
    return render_template("register.html.j2", message=message)

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

if __name__ == '__main__':
        app.run(debug=True, host="0.0.0.0", port=5000)
