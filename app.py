import os, time
from flask import Flask, jsonify, request
from script import selenium

app = Flask(__name__)
browser = selenium()

@app.route("/antecedentes", strict_slashes=False) #
def get_antecedentes():
    ci = request.args.get('ci')
    return jsonify(browser.run(ci))

if __name__ == "__main__":
    app.run(debug = True, host  = '0.0.0.0', port = 8080)