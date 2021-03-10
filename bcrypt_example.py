from flask import Flask, render_template, request, jsonify
from functools import wraps
import mysql.connector
import bcrypt
import configparser
import io


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

config = configparser.ConfigParser()
config.read('secrets.cfg')
PEPPER = config['secrets']['PEPPER']
DB_NAME = 'passwords'
DB_USERNAME = config['secrets']['DB_USERNAME']
DB_PASSWORD = config['secrets']['DB_PASSWORD']

@app.route('/')
def index():
    # print(PEPPER)
    return app.send_static_file('index.html')

# -------------------------------- API ROUTES ----------------------------------

@app.route('/api/signup', methods=['POST'])
def signup ():
    print(request.data)
    body = request.get_json()
    print(body)

    username = body['username']
    password = body['password'] + PEPPER
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    connection = mysql.connector.connect(user=DB_USERNAME, database=DB_NAME, password=DB_PASSWORD)
    cursor = connection.cursor()

    query = "INSERT into users (username, password) VALUES (%s, %s)"

    try:
        cursor.execute(query, (username, hashed))
        connection.commit()
        return {}
    except Exception as e:
        print(e)
        return {"username": username}, 302
    finally:
        cursor.close()
        connection.close()


@app.route('/api/login', methods=['POST'])
def login ():
    print(request.data)
    body = request.get_json()
    print(body)

    username = body['username']
    password = body['password'] + PEPPER

    connection = mysql.connector.connect(user=DB_USERNAME, database=DB_NAME, password=DB_PASSWORD)
    cursor = connection.cursor()

    query = "SELECT password FROM users WHERE username=%s"

    try:
        cursor.execute(query, (username,))
        hashed = cursor.fetchone()[0]
        print(hashed)
        success = bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        print(success)

        if success:
            return {}
        return {}, 404
    except Exception as e:
        print(e)
        return {}, 404
    finally:
        cursor.close()
        connection.close()
