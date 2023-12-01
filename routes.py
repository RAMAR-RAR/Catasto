from flask import render_template, request, redirect, flash, url_for
from bson import ObjectId
import config


@app.route("/")
def get_info():
    info=[]
    for dati in config.db.info_flask.find():
        dati['_id']= str(dati['_id'])
        info.append(dati)
    return render_template ('index.html', info=info)
    

if __name__ == '__main__':
    app.run(debug=True)