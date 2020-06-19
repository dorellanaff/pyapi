import os, time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Firefox, FirefoxOptions, FirefoxProfile, Chrome
from app import app
from app.script import selenium
from flask import Flask, jsonify, request, render_template, abort
from PyPDF2 import PdfFileWriter, PdfFileReader


browser = selenium()

def get_antecedentes(id):
    while True:
        if browser.wait == True:
            status = browser.antecedentes(id)
            if status[0]:
                print(status)
                re = pdf_reader(id, status[1], status[2])
                return jsonify(re), 200
            else:
                return jsonify(error="Timeout exceeded"), 500

def get_placainfo(id):
    while True:
        if browser.wait == True:
            status = browser.ant(id)
            if status[0]:
                print(status)
                return jsonify(status[1]), status[2]
            else:
                return jsonify(error="Timeout exceeded"), status[2]

def get_luzinfo(p, op):
    while True:
        if browser.wait == True:
            status = browser.luz(p, op)
            if status[0]:
                print(status)
                return jsonify(status[1]), status[2]
            else:
                return jsonify(error="Timeout exceeded"), status[2]

def get_cntinfo(p, op):
    while True:
        if browser.wait == True:
            status = browser.luz(p, op)
            if status[0]:
                print(status)
                return jsonify(status[1]), status[2]
            else:
                return jsonify(error="Timeout exceeded"), status[2]

def pdf_reader(id, url, path):
    pdffile = open(path, "rb")
    pdfread = PdfFileReader(pdffile)
    page = pdfread.getPage(0)
    pageContent = page.extractText()
    content = str(pageContent).splitlines()
    re = {
        'Fecha de Emision': content[0],
        'Numero de Certificado': content[1],
        'Tipo de Documento': content[2],
        'No de Identificacion': content[3],
        'Apellidos y Nombres': content[4],
        'Registra Antecedentes': content[5],
        'URL': url
    }
    return re

@app.route("/api/antecedentes/ci/<p>", strict_slashes=False) #
def ci_antecedentes(p):
    if len(p) == 10 and type(p) is str:
        ci = parameter
        print('Buscando Cedula. {}'.format(ci))
        return get_antecedentes(ci)
    return jsonify(error="Some parameters might not be correct"), 400

@app.route("/api/ant/placa/<p>", strict_slashes=False) #
def placa_ant(p):
    if len(p) == 7 and type(p) is str:
        placa = p
        print('Buscando Placa. {}'.format(placa))
        return get_placainfo(placa)
    return jsonify(error="Some parameters might not be correct"), 400

@app.route("/api/cnelep/ci/<p>", strict_slashes=False) #
def luz_cicnelep(p):
    if type(p) is str:
        ci = p
        print('Buscando Planilla Luz. CI {}'.format(ci))
        return get_luzinfo(ci, 1)
    return jsonify(error="Some parameters might not be correct"), 400

@app.route("/api/cnelep/contrato/<p>", strict_slashes=False) #
def luz_contratocnelep(p):
    if type(p) is str:
        contrato = p
        print('Buscando Planilla Luz. Contrato {}'.format(contrato))
        return get_luzinfo(contrato, 3)
    return jsonify(error="Some parameters might not be correct"), 400

@app.route("/api/cnelep/codigo/<p>", strict_slashes=False) #
def luz_codigocnelep(p):
    if type(p) is str:
        codigo = p
        print('Buscando Planilla Luz. Codigo {}'.format(codigo))
        return get_luzinfo(codigo, 2)
    return jsonify(error="Some parameters might not be correct"), 400

@app.route("/api/cnt/fijo/<p>", strict_slashes=False) #
def telefono_cnt(p):
    if type(p) is str:
        numero = p
        print('Buscando Planilla Telefono. {}'.format(numero))
        return get_cntinfo(numero, 2)
    return jsonify(error="Some parameters might not be correct"), 400

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404
