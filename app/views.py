import os, time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Firefox, FirefoxOptions, FirefoxProfile, Chrome
from app import app, q
from app.script import selenium
from flask import Flask, jsonify, request, render_template, abort

browser = selenium()

def get_antecedentes(id):
    while True:
        if browser.wait == True:
            re = browser.run(id)
            #job = q.enqueue_call(func=script.run, args=(ci,), timeout=-1)
            #id = job.get_id()
            print(re)
            return jsonify(re)

@app.route("/api", strict_slashes=False)
def api_doc():
    return "Documentacion"

@app.route("/api/ci/<id>", strict_slashes=False) #
def ci_antecedentes(id):
    if len(id) == 10 and type(id) is str:
        ci = id
        print('Buscando Cedula. {}'.format(ci))
        return get_antecedentes(ci)
    return abort(400, description="Some parameters might not be correct")


@app.route("/api/passport/<id>", strict_slashes=False) #
def passport_antecedentes(id):
    if type(id) is str:
        passport = id
        print('Buscando Pasaporte. {}'.format(passport))
        return get_antecedentes(passport)
    return abort(400, description="Some parameters might not be correct")

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404
