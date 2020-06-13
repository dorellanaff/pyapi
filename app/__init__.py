from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# Settings
CORS(app) 

from app import views
