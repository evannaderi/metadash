from flask_app import server

@server.route('/')
def index():
    return "Hello, Flask!"