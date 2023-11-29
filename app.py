from flask import Flask, render_template

app= Flask (__name__)

@app.route ('/')
def home():
    building= db['catasto']
    return render_template ('index.html')



if __name__=='__main__':
    app.run(debug=True, port=4000)






from flask import Flask, render_template, request, redirect, url_for, flash, session
from config_ws import User, app, DataBase,Device,Action
from datetime import datetime
import pandas as pd
import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
from apscheduler.schedulers.background import BackgroundScheduler
import numpy as np
import matplotlib as plt

scheduler = BackgroundScheduler()

@app.route('/')
def home():
    return render_template('Index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        data = DataBase.get_user(user, password)  # valida credenciales
        dataDev = DataBase.obtain_device()  # obtiene los device de una lista
        if data is not None and data[5] == 1:  # si las credenciales del usuario son admin va al reporte
            return redirect('/report/')
        else:  # si no crea detaglio utente y la lista de devices
            if data:
                dettaglioUtente = {
                    "username": data[1],
                    "password": data[2],
                    "nascita": data[3],
                    "corso": data[4]
                }

                session['username'] = user
                session['password'] = password

                listDevice = []
                for itemDev in dataDev:
                    listDevice.append(Device(itemDev[0], itemDev[1], itemDev[2]))

                list_actions = DataBase.get_user_actions(user)
                context = None
                if list_actions is not None:
                    list_actions_user = []
                    for action in list_actions:
                        action_data = {
                            'id': action[0],
                            'value_state': action[1],
                            'intensity': action[2],
                            'battery': action[3],
                            'date': action[4],
                            'id_Dev': action[5],
                            'id_user': action[6]
                        }
                        list_actions_user.append(action_data)
                    if list_actions_user:
                        battery_values = [action['battery'] for action in list_actions_user]
                        intensity_values = [action['intensity'] for action in list_actions_user]
                        battery_coef = np.polyfit(range(len(battery_values)), battery_values, 2)
                        intensity_coef = np.polyfit(range(len(intensity_values)), intensity_values, 2)
                        num_predictions = 10
                        action_future = range(len(battery_values), len(battery_values) + num_predictions)
                        predicted_battery = [round(value) for value in np.polyval(battery_coef, action_future)]
                        predicted_intensity = [round(value) for value in np.polyval(intensity_coef, action_future)]

                        context = (list(action_future), predicted_battery, predicted_intensity)

                        return render_template('dettaglio.html', dettaglioUtente=dettaglioUtente, listDevice=listDevice, list_actions=list_actions_user, context=context)
                    else:
                        message = "No se encontraron acciones para el usuario."
                        return render_template('dettaglio.html', dettaglioUtente=dettaglioUtente, error=message, listDevice=listDevice, list_actions=[], context=context)
                else:
                    message = "No se encontraron acciones para el usuario."
                    return render_template('dettaglio.html', dettaglioUtente=dettaglioUtente, error=message, listDevice=listDevice, list_actions=[], context=context)

    return render_template('login.html')



@app.route ('/registro')
def registro():
    return render_template ('registro.html')

@app.route('/add_registro', methods=['POST'])
def add_registro():    
    if request.method =='POST':
        user = request.form['user']
        password = request.form['password']
        nascita = request.form['nascita']
        corso = request.form['corso']
        is_admin = request.form.get('admin') == '1'

        usuario = User(user, password, nascita, corso,is_admin)
        DataBase.insert_user(usuario)
        context = None
        dataDev = DataBase.obtain_device()
        listDevice = []
        for itemDev in dataDev:
            listDevice.append(Device(itemDev[0], itemDev[1], itemDev[2]))

        return render_template('dettaglio.html', dettaglioUtente=usuario,listDevice=listDevice,context=context if context else None)

@app.route('/dettaglio')
def dettaglio():        
    return render_template('dettaglio.html')
    
@app.route('/device', methods=['GET','POST'])
def add_action():
    if request.method == 'GET':
        device_id = request.args.get('deviceId')       
        if device_id is not None: 
            id = int(device_id)
        else: id = None
        device = DataBase.getDeviceById(id)
        if device:
            objDevice = Device(device.get('id'), device.get('device'), device.get('stanza'))
            return render_template("device.html", device=objDevice)
        else:
            
            return "Device not found"

    elif request.method=='POST':
       date= datetime.now()
       id_Dev = 1 # Prof. Lezzi Non ho finito di definire la logica della programmazione delle azioni
       intensity = request.form.get('brightness')
       battery= 100-(int(intensity)* 5)#inicalmente 2 ahora 5
       scheduled_date=request.form.get('scheduled_date')#campo nuevo
       if scheduled_date is None:
           scheduled_date=date
       pending=request.form.get('pending')#campo nuevo
       if pending is None:
           pending=0
       else: pending=1

       username=session.get('username')
       password=session.get('password')
       user = DataBase.get_user(username, password)
       if user:
            id_user = user[0]
            value_state = request.form.get('check')
            if value_state is None:
                value_state = "0"
            else:
                value_state = "1"
            data = Action(value_state, intensity, battery, date, id_Dev, id_user,scheduled_date,pending)
            DataBase.control_device(data)
            return redirect('/device?deviceId=' + str(id_Dev))
       else: 
           return "Invalid user"
    else:
        return render_template("device.html")
    
@app.route('/logout')
def logout():
    return redirect(('/'))

@app.route('/program', methods=['GET', 'POST']) # Prof. Lezzi Non ho finito di definire la logica della programmazione delle azioni
def program():
       return render_template('program.html')

    
external_stylesheets = ['/static/stile.css']

app_d = dash.Dash(__name__, server=app, url_base_pathname='/report/', external_stylesheets=external_stylesheets)

app_d.layout = html.Div(
    className='container',
    children=[
        html.H1('Report'),
        dcc.Dropdown(
            id='my-dropdown',
            options=[],
            value=None
        ),
        dcc.Graph(
            id='intensity-graph',
            className='graph'
        ),
        dcc.Graph(
            id='battery-graph',
            className='graph'
        )
    ]
)



@app_d.callback( Output('my-dropdown', 'options'), Output('my-dropdown', 'value'), [Input('my-dropdown', 'search')])
def update_dropdown(search_value):
    results = DataBase.getDevice()
    options = [{'label': device[0], 'value': device[0]} for device in results]
    value=None
    return options, value

@app_d.callback(Output('intensity-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_drop_down_value):
    result = DataBase.request_graphic(selected_drop_down_value)
    dff = pd.DataFrame(result)
    dff.columns = ['Date', 'brigthness', 'Device', 'User']
    dff_filtered = dff[dff['Device'] == selected_drop_down_value]
    users = dff_filtered['User'].unique()
    colors = px.colors.qualitative.Plotly[:len(users)]
    fig = go.Figure()
    for i, user in enumerate(users):
        user_data = dff_filtered[dff_filtered['User'] == user]
        fig.add_trace(go.Scatter(x=user_data['Date'], y=user_data['brigthness'],
                                 name=user, line=dict(color=colors[i])))
    fig.update_layout(xaxis_title='Date', yaxis_title='Brightness')

    return fig

@app_d.callback(Output('battery-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_battery_graph(selected_drop_down_value):
    result = DataBase.request_battery_graph(selected_drop_down_value)  
    dff = pd.DataFrame(result)
    dff.columns = ['Date', 'battery_level', 'Device','User']
    dff_filtered = dff[dff['Device'] == selected_drop_down_value]
    users = dff_filtered['User'].unique()
    colors = px.colors.qualitative.Plotly[:len(users)]
    fig = go.Figure()
    for i, user in enumerate(users):
        user_data = dff_filtered[dff_filtered['User'] == user]
        fig.add_trace(go.Scatter(x=user_data['Date'], y=user_data['battery_level'],
                                 name=user, line=dict(color=colors[i])))
    fig.update_layout(xaxis_title='Date', yaxis_title='battery_level')
    return fig
    
if __name__ == '__main__':
    
    try:
        app.run(debug=True,host="0.0.0.0")
    except KeyboardInterrupt:
        DataBase.close()
