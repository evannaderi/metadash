from flask_app import server
from dash_app import app  # This import is needed even if it's unused; it initializes the Dash app

if __name__ == '__main__':
    server.run(debug=True)
