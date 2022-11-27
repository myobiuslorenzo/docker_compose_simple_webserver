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

app = Flask("webserver")


@app.route('/health', methods=['GET'])
def its_ok():
    return json.dumps({"status": "OK"})

def create_connection(config_):
    connection = None
    try:
        connection = mysql.connector.connect(**config_)
        print(connection)
        app.logger.info("Connection to MySQL DB successful")
    except Error as e:
        app.logger.info(f"The error '{e}' occurred")

    return connection


@app.route('/', methods=['GET'])
def execute_query():
    connection = create_connection(config)

    if connection is None:
        return flask.make_response("<head>connection failed</head>", 502)

    check = "SELECT * FROM users;"
    cursor = connection.cursor()

    if cursor is None:
        return flask.make_response("<head>cursor method failed</head>", 502)

    res = cursor.execute(check, multi=True)
    data = []
    for row in res:
        data.append(row.fetchall())
    return json.dumps(data)


def start():
    app.run(debug=True, host="0.0.0.0")


start()
