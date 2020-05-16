import os, time
from flask import Flask, jsonify, request, render_template
from script import selenium
from flask_cors import CORS
import redis
from rq import Queue

# Instantiation
r = redis.Redis()
q = Queue(connection=r)

app = Flask(__name__)
browser = selenium()

# Settings
CORS(app)

@app.route("/antecedentes", strict_slashes=False) #
def get_antecedentes():
    ci = request.args.get('ci')
    #re = browser.run(ci)
    task = q.enqueue_call(func=browser.run, args=(ci,), timeout=-1)
    print(str(task.get_id()))
    return render_template(task.get_id())

if __name__ == "__main__":
    app.run(debug = False, host  = '0.0.0.0', port = 8080)