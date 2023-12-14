from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
import pymongo
import json

app = Flask(__name__)

myClient = pymongo.MongoClient('mongodb+srv://BIGDATA1:BIGDATA1@bigdata1.atmuofo.mongodb.net/')
mydb = myClient['proveITSAR']
myCollection = mydb['catasto_geojson']
catasto_lines = mydb['catasto_lines']

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dati', methods=['GET', 'POST'])
def dati():
    if request.method == 'POST':
        print(request.form)
        if not request.form['cod_fisc'] == '':
            cod_fisc = request.form['cod_fisc']
            resultado = myCollection.find_one({"properties.cod_fisc": cod_fisc})
        else:
            print("Longitud ingresada")
            latitud = float(request.form['latitud'])
            longitud = float(request.form['longitud'])
            print(longitud)
            resultado = myCollection.find_one({ 
                'geometry.coordinates': {
                    '$elemMatch': {
                        '$elemMatch': {
                            '$elemMatch': {
                                '$eq': [latitud, longitud]
                            }
                        }
                    }
                }
            })       
        if resultado:
            clase = resultado['properties']['fclass']
            name = resultado['properties']['name']
            nome = resultado['properties']['nome']
            cognome = resultado['properties']['cognome']
            types = resultado['properties']['type']
            return render_template('dati.html', clase=clase, name=name, nome=nome, cognome=cognome, type=types)
        else:
            return render_template('dati.html', mensaje="No se encontraron datos para el código fiscal o las coordenadas proporcionadas.")
    return render_template('dati.html')

coordinates=[]
@app.route('/routes', methods=['GET', 'POST'])
def save_coord():
    global coordinates
    formatted_results=[]
    if request.method == 'POST':
        data = request.get_json()
        if 'coordinates' in data:
            received_coordinates = data['coordinates']
            coordinates.extend(received_coordinates)
            geo_coordinates = [[coord['lng'], coord['lat']] for coord in received_coordinates]
            results = myCollection.find({
                "geometry": {
                    "$geoIntersects": {
                        "$geometry": {
                            "type": "LineString",
                            "coordinates": geo_coordinates 
                        }
                    }
                }
            })
            formatted_results = []
            for doc in results:
                formatted_results.append({
                    'cod_fisc': doc['properties']['cod_fisc'],
                    'nome': doc['properties']['nome'],
                    'cognome': doc['properties']['cognome'],
                    'data_nascita': doc['properties']['data_nascita'],
                    'fclass': doc['properties']['fclass'],
                    'type': doc['properties']['type']
                    })
            formatted_results=json.dumps(formatted_results)
            print(formatted_results)
            return render_template('routes.html', raw_json=formatted_results)
        else:
            return jsonify(message='non ci sono proprietà in questa ruta')
    

    return render_template('routes.html')

if __name__ == '__main__':
    app.run(debug=True)

