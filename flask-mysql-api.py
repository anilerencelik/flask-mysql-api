from flask import Flask, make_response, jsonify, request
from mysql import connector
from mysql.connector import errorcode
from configparser import ConfigParser
import logging
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser()
config.read(f'{dir_path}/flask-mysql-api.cfg')
logging.basicConfig(filename=config['LOG']['FILE'], level=config['LOG']['LEVEL'])

def connect():
    return connector.connect(
        user=config['DB']['USER'],
        password=config['DB']['PASS'],
        host=config['DB']['HOST'],
        database=config['DB']['DB_NAME'],
        auth_plugin='mysql_native_password'
    )

def handleErrors(e):
    if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        logging.error(str(e))
        return('AUTH ERROR')
    elif e.errno == errorcode.ER_BAD_DB_ERROR:
        logging.error(str(e))
        return('DB NOT EXIST!')
    else:
        logging.error(str(e))
        return('ERROR DURING DB CONNECTION. CHECK LOG FILE')

def select(table):
    try:
        mysqlDB = connect()
        cursor = mysqlDB.cursor(buffered=True)
        db_name = config['DB']['DB_NAME']
        #query = f"SELECT * FROM {table};"
        query = f"SELECT * FROM {config['DB']['DB_NAME']}.{table};"
        cursor.execute(query)
        response = cursor.fetchall()
        mysqlDB.close()
        return response
    except Exception as e:
        return handleErrors(e)

def insert(tableName, name, lastname, email):
    try:
        mysqlDB = connect()
        cursor = mysqlDB.cursor(buffered=True)
        query = f"INSERT INTO {config['DB']['DB_NAME']}.{tableName} (name, lastname, email) VALUES ('{name}', '{lastname}', '{email}');"
        cursor.execute(query)
        mysqlDB.commit()
        mysqlDB.close()
        return 'SUCCESS'
    except Exception as e:
        return handleErrors(e)

def delete(tableName, id=None):
    try:
        mysqlDB = connect()
        cursor = mysqlDB.cursor(buffered=True)
        query = f"DELETE FROM {config['DB']['DB_NAME']}.{tableName}"
        if id:
            query += f" WHERE id={id}"
        query += ';'
        cursor.execute(query)
        mysqlDB.commit()
        mysqlDB.close()
        return 'SUCCESS'
    except Exception as e:
        return handleErrors(e)

app = Flask(__name__)

@app.route('/api/execute', methods=['GET'])
def selectEndpoint():
    tablename = request.args.get('tablename')
    if tablename is None:
        tablename = "USERS"
    response = select(tablename)
    if response and type(response) != type("s"):
        return jsonify(data=select(tablename))
    else:
        return make_response(jsonify(hata=response), 400)


@app.route('/api/execute', methods=['POST', 'PUT'])
def insertEndpoint():
    tablename = request.args.get('tablename')
    if tablename is None:
        tablename = "USERS"
    body = request.get_json()
    try:
        response = insert(tablename, body['name'], body['lastname'], body['email'])
        if response == 'SUCCESS':
            return jsonify(status=True, Message=response)
        else:
            return make_response(jsonify(hata=response), 400)
    except Exception as e:
        logging.error(str(e))
        return make_response(jsonify(info="Parametre isimleri dogru girilmeli" ,hata=str(e)), 400)

@app.route('/api/execute', methods=['DELETE'])
def deleteEndpoint():
    tablename = request.args.get('tablename')
    if tablename is None:
        tablename = "USERS"
    body = request.get_json()
    try:
        if type(body['id']) == type([1, 2]):
            
            for iterId in body['id']:
                print(iterId)
                response = delete(tablename, iterId)
                if response != 'SUCCESS':
                    return make_response(jsonify(hata=response), 400)
        else:
            response = delete(tablename, body['id'])
        if response == 'SUCCESS':
            return jsonify(status=True, Message=response)
        else:
            return make_response(jsonify(hata=response), 400)
    except Exception as e:
        logging.error(str(e))
        return make_response(jsonify(info="Parametre isimleri dogru girilmeli" ,hata=str(e)), 400)


if __name__ == '__main__':
    app.run(host=config['API']['HOST'], port=config['API']['PORT'], debug=False)
