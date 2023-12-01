from flask import Flask, render_template, request, redirect, url_for
import config import db

app=Flask(__name__)

@app.route('/')
def index():
    details= db['details']
    detailsReceived=buildings.find()
    return render_template('index.html',details = detailsReceived)

@app.route('/search', methods=['POST'])
def find_person():
    person=db['persons']
    name= request,form['name']
    
