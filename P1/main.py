import hashlib
import sqlite3
import json
import pandas as pd
from urllib.request import urlopen

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

cursor.execute("DROP TABLE legal")
cursor.execute("DROP TABLE users")

cursor.execute(
    "CREATE TABLE IF NOT EXISTS legal (nombrel,cookies,aviso,proteccion_de_datos,politicas,creacion,primary key(nombrel))")
cursor.execute(
    "CREATE TABLE IF NOT EXISTS users (nombre,telefono,password,provincia,permisos,total_emails,phishing_email,cliclados_email,probClick,fechas,num_fechas,ips,num_ips,passVul,primary key (nombre))")
insert_legal = """INSERT INTO legal (nombrel,cookies,aviso,proteccion_de_datos,politicas,creacion) VALUES (?,?,?,?,?,?)"""
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
    print("Media y desviación estándar\n")
    print("Media\n", dataFrame.mean(), "\n")
    print("Desviación\n", dataFrame.std(), "\n")
    print("Maximo y mínimo de total fechas\n")
    print("Maximo", dataFrame['Numero fechas'].max())
    print("Minimo", dataFrame['Numero fechas'].min())
    print("Maximo", dataFrame['Total Emails'].max())
    print("Minimo", dataFrame['Total Emails'].min())

def ejercicio3():
    query = con.execute("SELECT * From users where permisos  = 0")
    cols = [column[0] for column in query.description]
    dUsersUser = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)

    query = con.execute("SELECT * From users where permisos  = 1")
    cols = [column[0] for column in query.description]
    dUsersAdmin = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)

    query = con.execute("SELECT * From users where emailsPhising >= 200")
    cols = [column[0] for column in query.description]
    dUsersMas200 = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)

    query = con.execute("SELECT * From users where emailsPhising < 200")
    cols = [column[0] for column in query.description]
    dUsersMenos200 = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)


ejercicio2()
ejercicio3()
