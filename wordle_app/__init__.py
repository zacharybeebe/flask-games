from flask import Flask
from wordle_app.config.app_config import *
from wordle_app.models import *

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['GAME'] = get_new_game()

# Use this bool to control your app debug state, run.py will import this
DEBUG = True

from wordle_app.routes import routes
