from flask_app import server
from dash_app import app  # This import is needed even if it's unused; it initializes the Dash app

if __name__ == '__main__':
    server.run(debug=True, port=5001)

    # To user: run this file to start the server
    # After running, go to http://127.0.0.1:5001/dashboard in your browser

    # The github repo link is https://github.com/evannaderi/metadash
    # git stash
    # git pull
