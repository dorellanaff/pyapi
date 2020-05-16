from flask import Flask
from rq import Queue
from rq.job import Job
from worker import conn
from flask_cors import CORS

# Instantiation
q = Queue(connection=conn)

app = Flask(__name__)

# Settings
CORS(app) 

from app import views
