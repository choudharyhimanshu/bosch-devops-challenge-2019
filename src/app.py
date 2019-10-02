import os
from flask import Flask
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson.json_util import dumps
from faker import Faker
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
api = Api(app)
fake = Faker()

if os.environ["PORT"] is None:
    port = 5000
else:
    port = int(os.environ["PORT"])

if os.environ["DB_NAME"] is None:
    db_name = 'user_db'
else:
    db_name = os.environ["DB_NAME"]

if os.environ["MONGODB_CONNECTION_URL"] is None:
    db = None
else:
    db = MongoClient(os.environ["MONGODB_CONNECTION_URL"])[db_name]

def clear_db():
    if db is not None:
        db['users'].delete_many({})

def load_dummy_data():
    if db is not None:
        users = db['users']
        for i in range(10):
            users.insert_one({'name': fake.name(), 'email': fake.email()})

# @app.route('/')
# def hello_world():
#     return {'message': 'Hello, World!'}

@app.route('/')
def get_users():
    if db is None:
        return {'message': 'Error connecting DB'}, 500
    return dumps(db['users'].find({}, {'_id': False}))

if __name__ == '__main__':
    clear_db()
    load_dummy_data()
    app.run(port=port, debug=True, host='0.0.0.0')
