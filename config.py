#configurazione nel server # Patron DAO (Data Acces Object, per mantenere la persistenza dei dati)
from flask import Flask
from bson import ObjectId
from pymongo import MongoClient

app = Flask(__name__) 
client= MongoClient('mongodb+srv://BIGDATA1:BIGDATA1@bigdata1.atmuofo.mongodb.net/')
db=client.proveITSAR

def openClose():
    client = MongoClient('mongodb+srv://BIGDATA1:BIGDATA1@bigdata1.atmuofo.mongodb.net/')

    db = client["does-not-exist"]
    print(db)

    db = client.proveITSAR
    print(db)

    db = client["proveITSAR"]
    print(db)

    comments = db.comments
    print(comments)

    comments = db["comments"]
    print(comments)

    client.close()

def find():
    client = MongoClient('mongodb+srv://BIGDATA1:BIGDATA1@bigdata1.atmuofo.mongodb.net/')

    query = {
        "nome": "Giuseppe" 
    }
    projection = {
        
        "_id": 0
    }
    
    cursor = client.proveITSAR.catasto_ssg.find(filter=query,limit=1)

    for post in cursor:
        print(post)
       
    client.close()

if __name__ == '__main__':
    
    find()