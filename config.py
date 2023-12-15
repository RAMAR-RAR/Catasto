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
            resultados = myCollection.find({"properties.cod_fisc": cod_fisc})
        else:
            print("Longitud ingresada")
            latitud = float(request.form['latitud'])
            longitud = float(request.form['longitud'])
            print(longitud)
            resultados = myCollection.find({ 
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
        
        lista_resultados = []
        for resultado in resultados:
            clase = resultado['properties']['fclass']
            name = resultado['properties']['name']
            nome = resultado['properties']['nome']
            cognome = resultado['properties']['cognome']
            types = resultado['properties']['type']
            lista_resultados.append({
                'clase': clase,
                'name': name,
                'nome': nome,
                'cognome': cognome,
                'type': types
            })

        if lista_resultados:
            print(lista_resultados)
            return render_template('dati.html', resultados=lista_resultados)
        else:
            return render_template('dati.html', mensaje="No se encontraron datos para el código fiscal o las coordenadas proporcionadas.")

    return render_template('dati.html')

coordinates=[]
@app.route('/routes', methods=['GET','POST'])
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
            
            for result in results:
                clase = result['properties']['fclass']
                name = result['properties']['name']
                nome = result['properties']['nome']
                cognome = result['properties']['cognome']
                types = result['properties']['type']
                formatted_results.append({
                    'clase': clase,
                    'name': name,
                    'nome': nome,
                    'cognome': cognome,
                    'types': types
                })
        return (formatted_results)    
    return render_template('routes.html')

if __name__ == '__main__':
    app.run(debug=True)

