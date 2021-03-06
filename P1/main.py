import hashlib
import os
import sqlite3
import json
import pandas
import pandas as pd
from urllib.request import urlopen
import plotly.express as px
import plotly.utils
import plotly.graph_objects as go
import plotly.express as px
from fpdf import FPDF
from flask import Flask, render_template, request,redirect, session, app



fLegal = open('legal.json')
fUsers = open('users.json')
dataLegal = json.load(fLegal)
dataUsers = json.load(fUsers)


def probClick(cliclados, total):
    if (total != 0):
        return (cliclados / total) * 100
    else:
        return 0


def checkPass(password):
    md5hash = password
    try:
        password_list = str(urlopen(
            "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt").read(),
                            'utf-8')
        for password in password_list.split('\n'):
            guess = hashlib.md5(bytes(password, 'utf-8')).hexdigest()
            if guess == md5hash:
                return 1
                break
            elif guess != md5hash:
                continue
            else:
                return 2
        return 2
    except Exception as exc:
        return 2


con = sqlite3.connect('PRACTICA1.DB')
cursor = con.cursor()

'''cursor.execute("DROP TABLE legal")
cursor.execute("DROP TABLE users")

cursor.execute(
    "CREATE TABLE IF NOT EXISTS legal (nombrel,cookies,aviso,proteccionDatos,politicas,creacion,primary key(nombrel))")
cursor.execute(
    "CREATE TABLE IF NOT EXISTS users (nombre,telefono,password,provincia,permisos,total_emails,phishing_email,cliclados_email,probClick,fechas,num_fechas,ips,num_ips,passVul,primary key (nombre))")
insert_legal = """INSERT INTO legal (nombrel,cookies,aviso,proteccionDatos,politicas,creacion) VALUES (?,?,?,?,?,?)"""
insert_users = """INSERT INTO users (nombre,telefono,password,provincia,permisos,total_emails,phishing_email,cliclados_email,probClick,fechas,num_fechas,ips,num_ips,passVul) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""

for i in dataLegal['legal']:
    for j in i.keys():
        for k in i.values():
            dLegal = (
                j, k['cookies'], k['aviso'], k['proteccion_de_datos'],
                k['cookies'] + k['aviso'] + k['proteccion_de_datos'],
                k['creacion'])
        cursor.execute(insert_legal, dLegal)
        con.commit()

for i in dataUsers['usuarios']:
    for j in i.keys():
        for k in i.values():
            dUsers = (j, k['telefono'], k['contrasena'], k['provincia'], k['permisos'], k['emails']['total'],
                      k['emails']['phishing'], k['emails']['cliclados'],
                      probClick(k['emails']['cliclados'], k['emails']['phishing']), str(k['fechas']), len(k['fechas']),
                      str(k['ips']), len(k['ips']), checkPass(k['contrasena']))
        cursor.execute(insert_users, dUsers)
        con.commit()

con.commit()
'''
dataFrame = pd.DataFrame()


def ejercicio2():
    cursor.execute('SELECT num_fechas FROM users')
    cols = cursor.fetchall()
    resultado = []
    for i in cols:
        resultado += [i[0]]
    dataFrame['Numero fechas'] = resultado

    cursor.execute('SELECT num_ips FROM users')
    cols = cursor.fetchall()
    resultado = []
    for i in cols:
        resultado += [i[0]]
    dataFrame['Numero IPS'] = resultado

    cursor.execute('SELECT num_fechas FROM users')
    cols = cursor.fetchall()
    resultado = []
    for i in cols:
        resultado += [i[0]]
    dataFrame['Numero IPS'] = resultado

    cursor.execute('SELECT total_emails FROM users')
    cols = cursor.fetchall()
    resultado = []
    for i in cols:
        resultado += [i[0]]
    dataFrame['Total Emails'] = resultado

    print("EJERCICIO 2\n")
    print("Numero de muestras")
    print(dataFrame.count(), "\n")
    print("Media y desviaci??n est??ndar\n")
    print("Media\n", dataFrame.mean(), "\n")
    print("Desviaci??n\n", dataFrame.std(), "\n")
    print("Maximo y m??nimo de total fechas\n")
    print("Maximo", dataFrame['Numero fechas'].max())
    print("Minimo", dataFrame['Numero fechas'].min())
    print("Maximo", dataFrame['Total Emails'].max())
    print("Minimo", dataFrame['Total Emails'].min())

dfUsuarios = pd.DataFrame()
dfAdmins = pd.DataFrame()
dfMenor200 = pd.DataFrame()
dfMayor200 = pd.DataFrame()
totalDF = pd.DataFrame()


def ejercicio3():


    cursor.execute('SELECT phishing_email FROM users where permisos="0"')
    rows = cursor.fetchall()
    res = []
    for i in rows:
        res += [i[0]]
    dfUsuarios['Phishing Emails Permisos Usuario'] = res

    cursor.execute('SELECT phishing_email FROM users where permisos="1"')
    rows = cursor.fetchall()
    res = []
    for i in rows:
        res += [i[0]]
    dfAdmins['Phishing Emails Permisos Admin'] = res

    cursor.execute('SELECT phishing_email FROM users where total_emails<200')
    rows = cursor.fetchall()
    res = []
    for i in rows:
        res += [i[0]]
    dfMenor200['Phishing Emails De Gente con < 200 correos'] = res

    cursor.execute('SELECT phishing_email FROM users where total_emails>=200')
    rows = cursor.fetchall()
    res = []
    for i in rows:
        res += [i[0]]
    dfMayor200['Phishing Emails de Gente >= 200 correos'] = res

    print("\nEJERCICIO 3\n")
    print("Phishing Emails de Permisos Usuario\n")
    print(dfUsuarios.describe())
    print(dfUsuarios)
    num_missing = dfUsuarios.isna().sum()
    print("Valores Missing de", num_missing)
    print("\n")

    print("Phishing Emails de Permisos Administrador\n")
    print(dfAdmins.describe())
    print(dfAdmins)
    num_missing = dfAdmins.isna().sum()
    print("Valores Missing de", num_missing)
    print("\n")

    print("Phishing Emails de Personas con menos de 200 correos\n")
    print(dfMenor200.describe())
    print(dfMenor200)
    num_missing = dfMenor200.isna().sum()
    print("Valores Missing de", num_missing)
    print("\n")

    print("Phishing Emails de Personas con mas o igual de 200 correos\n")
    print(dfMayor200)
    print(dfMayor200.describe())
    num_missing = dfMayor200.isna().sum()
    print("Valores Missing de", num_missing)
    print("\n")

    totalDF = pd.concat([dfAdmins,dfUsuarios,dfMayor200,dfMenor200],axis = 1)
    print("Numero de Observaciones\n")
    print(totalDF.count(),"\n")
    print("Numero de valores Missing\n")
    print(totalDF.isna().sum(),"\n")
    print("Medianas\n")
    print(totalDF.median(),"\n")
    print("Medias\n")
    print(totalDF.mean(),"\n")
    print("Desviaciones\n")
    print(totalDF.std(),"\n")
    print("Maximos\n")
    print(totalDF.max(),"\n")
    print("Minimos\n")
    print(totalDF.min(),"\n")



dfLegal = pd.DataFrame()
dfPrivacidad = pd.DataFrame()
dfVulnerable = pd.DataFrame()
dfConexiones = pd.DataFrame()
dfCritico = pd.DataFrame()



def ejercicio4():
    cursor.execute('SELECT nombrel, cookies, aviso, proteccionDatos FROM legal ORDER BY politicas limit 5')
    cols = cursor.fetchall()
    nombre = []
    cookies = []
    avisos = []
    proteccionDatos = []
    for i in range(len(cols)):
        nombre += [cols[i][0]]
        cookies += [cols[i][1]]
        avisos += [cols[i][2]]
        proteccionDatos += [cols[i][3]]
    dfLegal['Nombre'] = nombre
    dfLegal['Cookies'] = cookies
    dfLegal['Avisos'] = avisos
    dfLegal['Proteccion de Datos'] = proteccionDatos

    fig = go.Figure(data=[
        go.Bar(name='Cookies', x=dfLegal['Nombre'], y=dfLegal['Cookies'], marker_color='steelblue'),
        go.Bar(name='Avisos', x=dfLegal['Nombre'], y=dfLegal['Avisos'], marker_color='lightsalmon'),
        go.Bar(name='Proteccion de datos', x=dfLegal['Nombre'], y=dfLegal['Proteccion de Datos'], marker_color='red')
    ])

    fig.update_layout(title_text="Cinco peores webs", title_font_size=41, barmode='group')
    plotly.io.write_image(fig, file='pltxWeb.png', format='png', width=700, height=450)

    cursor.execute('SELECT DISTINCT creacion FROM legal ORDER BY creacion')
    cols = cursor.fetchall()
    creacion = []
    for i in range(len(cols)):
        creacion += [cols[i][0]]
    dfPrivacidad['Creacion'] = creacion

    cursor.execute('SELECT creacion, proteccionDatos FROM legal WHERE proteccionDatos=1 ORDER BY creacion')
    cols = cursor.fetchall()
    seCumple = [0]*len(creacion)
    for i in range(len(creacion)):
        for j in range(len(cols)):
            if cols[j][0] == creacion[i]:
                seCumple[i] += 1
    dfPrivacidad['Se cumple'] = seCumple

    cursor.execute('SELECT creacion, proteccionDatos FROM legal WHERE proteccionDatos=0 ORDER BY creacion')
    cols = cursor.fetchall()
    noSeCumple = [0] * len(creacion)
    for i in range(len(creacion)):
        for j in range(len(cols)):
            if cols[j][0] == creacion[i]:
                noSeCumple[i] += 1
    dfPrivacidad['No se cumple'] = noSeCumple

    fig = go.Figure(data=[
        go.Bar(name='Se cumple', x=dfPrivacidad['Creacion'], y=dfPrivacidad['Se cumple'], marker_color='steelblue'),
        go.Bar(name='No se cumple', x=dfPrivacidad['Creacion'], y=dfPrivacidad['No se cumple'], marker_color='lightsalmon')
    ])

    fig.update_layout(title_text="Privacidad segun el A??o de Creaci??n", title_font_size=41, barmode='group')
    plotly.io.write_image(fig, file='pltxPrivacidad.png', format='png', width=700, height=450)


    cursor.execute('SELECT COUNT(num_ips) FROM users where num_ips>=10')
    cols = cursor.fetchall()
    resultado = []
    for i in cols:
        resultado += [i[0]]
    dfVulnerable['Comprometidas'] = resultado

    cursor.execute('SELECT COUNT(num_ips) FROM users where num_ips<10')
    cols = cursor.fetchall()
    resultado = []
    for i in cols:
        resultado += [i[0]]
    dfVulnerable['No Comprometidas'] = resultado

    labels = ['No Comprometidas', 'Comprometidas']
    values = [dfVulnerable.at[0, 'No Comprometidas'], dfVulnerable.at[0, 'Comprometidas']]
    fig = go.Figure(data=[
        go.Pie(labels=labels, values=values)])
    fig.update_layout(title_text="Comparaci??n de contrase??as", title_font_size=41, barmode='group')
    plotly.io.write_image(fig, file='pltxContrase??as.png', format='png', width=700, height=450)

    cursor.execute('SELECT AVG (num_ips) FROM users where passVul=1')
    cols = cursor.fetchall()
    resultado = []
    for i in cols:
        resultado += [i[0]]
    dfConexiones['Vulnerables'] = resultado

    cursor.execute('SELECT AVG(num_ips) FROM users where passVul=2')
    cols = cursor.fetchall()
    resultado = []
    for i in cols:
        resultado += [i[0]]
    dfConexiones['No Vulnerables'] = resultado

    labels = ['Vulnerables', 'No Vulnerables']
    values = [dfConexiones.at[0, 'Vulnerables'], dfConexiones.at[0, 'No Vulnerables']]
    fig = go.Figure(data=[
        go.Pie(labels=labels, values=values)])
    fig.update_layout(title_text="Media de conexiones de usuarios", title_font_size=41, barmode='group')
    plotly.io.write_image(fig, file='pltxMediaConexiones.png', format='png', width=700, height=450)


    cursor.execute('SELECT nombre,probClick FROM users where passVul=1 ORDER BY probClick DESC LIMIT 10')
    cols = cursor.fetchall()
    resultado = []
    for i in cols:
        resultado += [i[0]]

    nombre = []
    prob = []
    for i in range(len(cols)):
        nombre += [cols[i][0]]
        prob += [cols[i][1]]
    dfCritico['Nombre'] = nombre
    dfCritico['Probabilidad de Click'] = prob
    fig = px.bar(dfCritico, x=dfCritico['Nombre'], y=dfCritico['Probabilidad de Click'])
    fig.update_layout(title_text="Usuarios m??s cr??ticos", title_font_size=41, barmode='group')
    plotly.io.write_image(fig, file='pltxUsers.png', format='png', width=700, height=450)

ejercicio2()
ejercicio3()
ejercicio4()


con.close()

