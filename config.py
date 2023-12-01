from pymongo import MongoClient
from flask import Flask
from flask_pymongo import PyMongo
import pymongo

app = Flask(__name__)

myClient= pymongo.MongoClient('mongodb+srv://BIGDATA1:BIGDATA1@bigdata1.atmuofo.mongodb.net/')
mydb=myClient['proveITSAR']
myCollection=mydb['catasto_geojson']

cod_fisc = input("Inserisci il codice fiscale: ")
resultado = myCollection.find_one({"properties.cod_fisc": cod_fisc})
if resultado:
    print("Clase:", resultado['properties']['fclass'])
    print("name:", resultado['properties']['name'])
    print("Nome:", resultado['properties']['nome'])
    print("Cognome:", resultado['properties']['cognome'])
else:
    print("No se encontraron datos para el código fiscal proporcionado.")
