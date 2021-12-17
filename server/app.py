from flask import *
from elasticsearch import Elasticsearch
import time
from datetime import datetime
import json
import random
from es_client import es_client
import priviledge_provider #module created 

fake_db = []
app = Flask(__name__)

@app.route('/')
def index():
    return "OK"

@app.route('/auth', methods=["GET", "POST"])
def auth():
    jwt_token = priviledge_provider.authenticate_user(request.json)
    return jwt_token


@app.route('/get-cards') #not a practice in prod-env
@priviledge_provider.check_path_priviledge
def get_cards():
    es_client.addEntry(request, 200)
    return json.dumps(fake_db)

@app.route('/get-card')
@priviledge_provider.check_path_priviledge
@priviledge_provider.check_obj_priviledge(category="cards") #add here category in order to know in that table to look for there will be a pair as uuid - (category aka table and id which is unique in the table)
def get_card():
    for datum in fake_db:
        if str(datum["id"]) == str(request.args.get('id')):
            es_client.addEntry(request, 200)
            return json.dumps(datum, indent=2)

    es_client.addEntry(request, 404)
    return {"status": "Not found"}

@app.route('/create-card', methods=["POST"])
@priviledge_provider.check_path_priviledge
@priviledge_provider.generate_obj_priviledge(category="cards")
def create_card():
    global fake_db

    user_data = request.json
    user_data["card_number"] = random.randint(100000,9999999)
    user_data["id"] = random.randint(1,200)
    fake_db.append(user_data)
    es_client.addEntryJson(request, user_data, 200)
    return json.dumps(user_data)

@app.route('/delete-card', methods=["DELETE"])
@priviledge_provider.check_path_priviledge
@priviledge_provider.generate_obj_priviledge(category="cards")
def delete_card():
    print("Deleting the card master")    
    es_client.addEntry(request, 200)
    return {"card_status": "deleted"}

@app.route('/obj_priviledge', methods=["GET", "POST"])
@priviledge_provider.check_obj_priviledge_to_alter
def obj_show():
    pass

if __name__ == '__main__':
    es_client.initDB()
    app.run(host='0.0.0.0', port=5000, debug=True)
