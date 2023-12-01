from pymongo import MongoClient
from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import pymongo

app = Flask(__name__)

myClient= pymongo.MongoClient('mongodb+srv://BIGDATA1:BIGDATA1@bigdata1.atmuofo.mongodb.net/')
mydb=myClient['proveITSAR']
myCollection=mydb['catasto_geojson']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cod_fisc = request.form['cod_fisc']
        resultado = myCollection.find_one({"properties.cod_fisc": cod_fisc})
        if resultado:
            clase = resultado['properties']['fclass']
            name = resultado['properties']['name']
            nome = resultado['properties']['nome']
            cognome = resultado['properties']['cognome']
            types = resultado['properties']['type']
            return render_template('index.html', clase=clase, name=name, nome=nome, cognome=cognome, type=types)
        else:
            return render_template('index.html', mensaje="No se encontraron datos para el código fiscal proporcionado.")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
