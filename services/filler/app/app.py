import flask
from flask import Flask, request
import mysql.connector
from mysql.connector import Error
import pandas as pd
from multiprocessing import Process
import logging
import json

logging.basicConfig(level=logging.DEBUG)

config = {
    'user': 'root',
    'password': 'password',
    'host': 'db',
    'port': '3306',
    'database': 'mysql_database'
}

app = Flask("database_filler_script")
data = pd.read_csv("data.csv")
name_col = data['name'].to_numpy().tolist()
age_col = data['age'].to_numpy().tolist()


def create_connection(config_):
    connection = None
    try:
        connection = mysql.connector.connect(**config_)
        print(connection)
        app.logger.info("Connection to MySQL DB successful")
    except Error as e:
        app.logger.info(f"The error '{e}' occurred")

    return connection


@app.route('/', methods=['GET', 'POST'])
def execute_query():
    connection = create_connection(config)

    if connection is None:
        return flask.make_response("<head>connection failed</head>", 502)

    query = "INSERT INTO users ( name, age ) VALUES ( %s, %s );"
    check = "SELECT * FROM users;"
    cursor = connection.cursor()

    if cursor is None:
        return flask.make_response("<head>cursor method failed</head>", 502)

    cursor.executemany(query, list(zip(name_col, age_col)))
    connection.commit()
    res = cursor.execute(check, multi=True)

    app.logger.info("Query executed successfully")
    app.logger.info(res)
    app.logger.info("THIS IS THE DATA FROM USERS TABLE: ")
    for row in res:
        app.logger.info(row.fetchall())


    return json.dumps({"status": "OK"})

# @app.route("/shutdown", methods=['GET'])
# def shutdown():
#     shutdown_func = request.environ.get('werkzeug.server.shutdown')
#     if shutdown_func is None:
#         raise RuntimeError('Not running werkzeug')
#     shutdown_func()
#     return "Shutting down..."


def start():
    app.run(debug=True, host="0.0.0.0")

# def stop():
#     import requests
#     return requests.get('http://localhost:5000/shutdown')

start()
# stop()
# def main():
#     #app.run(debug=True, host="0.0.0.0")
#
#     server = Process(target=app.run, args=(True, "0.0.0.0"))
#     server.start()
#     #
#     server.terminate()
#     server.join()
#
# main()
