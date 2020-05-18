import os, time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Firefox, FirefoxOptions, FirefoxProfile, Chrome
from app import app, q
from app.script import selenium
from flask import Flask, jsonify, request, render_template

browser = selenium()

@app.route("/api", strict_slashes=False) #
def get_antecedentes():
    ci = request.args.get('ci')
    print('Buscando {}'.format(ci))
    while True:
        if browser.wait == True:
            re = browser.run(ci)
            #job = q.enqueue_call(func=script.run, args=(ci,), timeout=-1)
            #id = job.get_id()
            print(re)
            return re
