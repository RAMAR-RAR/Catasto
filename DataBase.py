from pymongo import MongoClient
import certifi
from flask import Flask

MONGO_URI= 'mongodb+srv://BIGDATA1:BIGDATA1@bigdata1.atmuofo.mongodb.net/'
ca= certifi.where()

class DevelopmentConfig:
    DEBUG=True

class Building:
    def __init__(self, area, autonomous_region, description, has_storage, is_residential,latitude, longitude): # Se ejecuta automáticamente cuando se crea una nueva instancia de la clase.
        self.area = area #atributos de la clase (publicos por defecto)
        self.autonomus_region = autonomus_region
        self.description = description
        self.has_storage = has_storage
        self.is_residential=is_residential

description
has_storage
is_residential
latitude
longitude
neighbors_per_floor
number
postal_code
province
reference
street
total_floors
town
typology
year_built


def dbConection():
    try:
        client= MongoClient.connect(MONGO_URI,tlsCAFile=ca)
        db=client ['proveITSAR']
    except ConnectionError:
        print('Errore di conessione')
    return db
