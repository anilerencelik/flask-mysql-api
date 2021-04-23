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


if __name__ == '__main__':
    print(insert("USERS"))