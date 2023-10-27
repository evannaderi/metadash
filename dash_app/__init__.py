import dash
from flask_app import server
import os, sys

print("Current working directory:", os.getcwd())
app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')

from dash_app import layout