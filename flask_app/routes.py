from flask_app import server
from flask import send_file
import os

@server.route('/')
def index():
    return "Hello, Flask!"

@server.route('/hello')
def serve_image():
    print("Current working directory:", os.getcwd())
    file_path = 'clock.png'
    return send_file(file_path, mimetype='image/png')
    