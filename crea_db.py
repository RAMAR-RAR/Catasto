import pandas as pd
from datetime import datetime, timedelta
import random
import re
import numpy as np
from numpy import size

def extrae_consonanti(text):
    return re.sub(r'[^bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]+','', text)


file=r"C:\Users\JuliaElenaSilloCondo\OneDrive - ITS Angelo Rizzoli\Documenti\DATALAKE2\Catasto\nomi_fict.csv"
df= pd.read_csv(file,header=0, sep=';', encoding='latin-1')
df=df.dropna(subset=['nome'])

#########################
#Crear una columna con fechas de nacimiento aleatorias
data_nascita=[]
for i in range(len(df)):
    data_nasc=datetime.now()- timedelta(days=random.randint(365*18,365*60))
    data_nascita.append(data_nasc)
df['data_nascita']=data_nascita

# Crear una nueva columna con las consonantes del apellido ---> reducir a tres letras las consonantes
df['c_nome']=(df['nome'].apply(extrae_consonanti)).str.upper()
df['c_cognome']=(df['cognome'].apply(extrae_consonanti)).str.upper()

# Adecuar la fecha de nacmiento
df['anno_nascita']=df['data_nascita'].dt.year.astype(str).str[2:]
meses={1:'A',2:'B',3:'C',4:'D',5:'E',6:'H',7:'L',8:'M',9:'P',10:'R',11:'S',12:'T'}
df['mese_nascita']=df['data_nascita'].dt.month.map(meses)
#Llenar aleatoriamente con M o F para identificar el sexo
df['genere']=np.random.choice([0,40],len(df))
df['giorno_nascita']=df['data_nascita'].dt.day
# crear una columna con el codice fiscale
df['num_giorno']=df['giorno_nascita']+df['genere']
df['num_giorno']=df['num_giorno'].astype(str)
print(df.dtypes)
df['cod_fisc']=df['c_cognome']+df['c_nome']+df['anno_nascita']+df['mese_nascita']+df['num_giorno']+df['nascita']
df['num']=np.random.randint(1,101, size=len(df))
df['year_built']=np.random.randint(1900,2020, size=len(df))
df['total_floors']=np.random.randint(1,10, size=len(df))

df.to_csv('nomi_fict_2.csv')
file2=r"C:\Users\JuliaElenaSilloCondo\OneDrive - ITS Angelo Rizzoli\Documenti\DATALAKE2\Catasto\comune_ssg.csv"
df2= pd.read_csv(file2,header=0, sep=',', encoding='latin-1')

print(df2.dtypes)
df_catasto=pd.merge(df,df2,on='osm_id')
df_catasto.to_csv('catasto.csv')






