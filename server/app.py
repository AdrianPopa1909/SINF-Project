from flask import *
from elasticsearch import Elasticsearch
import time
from datetime import datetime
import json
import random
# import priviledge_provider #module created 

fake_db = []
app = Flask(__name__)
es_client = Elasticsearch(['http://elastic_search:9200/'], verify_certs=True)
es_index_name = "sinf_index"
es_index = 0

@app.route('/')
def index():
    return "OK"

@app.route('/auth', methods=["GET", "POST"])
def auth():
    jwt_token = priviledge_provider.authenticate_user(request.json)
    return jwt_token


@app.route('/get-cards') #not a practice in prod-env
# @priviledge_provider.check_path_priviledge
def get_cards():
    return json.dumps(fake_db)

@app.route('/get-card')
# @priviledge_provider.check_path_priviledge
# @priviledge_provider.check_obj_priviledge(category="cards") #add here category in order to know in that table to look for there will be a pair as uuid - (category aka table and id which is unique in the table)
def get_card():
    add_entry_db(request.args, 200)
    for datum in fake_db:
        if str(datum["id"]) == str(request.args.get('id')):
            return json.dumps(datum, indent=2)
    return {"status": "Not found"}

@app.route('/create-card', methods=["POST"])
# @priviledge_provider.check_path_priviledge
# @priviledge_provider.generate_obj_priviledge(category="cards")
def create_card():
    global fake_db

    user_data = request.json
    user_data["card_number"] = random.randint(100000,9999999)
    user_data["id"] = random.randint(1,200)
    fake_db.append(user_data)
    return json.dumps(user_data)

@app.route('/delete-card', methods=["DELETE"])
# @priviledge_provider.check_path_priviledge
# @priviledge_provider.generate_obj_priviledge(category="cards")
def delete_card():
    print("Deleting the card master")    
    return {"card_status": "deleted"}

@app.route('/obj_priviledge', methods=["GET", "POST"])
# @priviledge_provider.check_obj_priviledge_to_alter
def obj_show():
    pass

def add_entry_db(arguments, status):
    global es_index_name
    global es_index

    entry = dict()
    entry['query_arguments'] = " ".join([x + ":" + y for x, y in arguments.items()])
    entry['response_status'] = status
    entry['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("New entry: %s"%entry)

    json_data = json.dumps(entry)
    result = es_client.index(index=es_index_name, id=es_index, document=json_data)
    print("Updating the client index %s"%result)
    es_index = es_index + 1
    
def init_db():
    global es_index_name
    global es_index

    while not es_client.ping():
        print('elastic search db not responfing')
        time.sleep(5)
    print('elastic search db is up')

    el_config_file = open("elastic_seach_mapping.json", "r")
    el_config = json.load(el_config_file)


    exists = es_client.indices.exists(index=es_index_name)
    if exists:
            result = es_client.indices.put_mapping(index=es_index_name, body=el_config["mappings"])
            print('Updating mapping: %s'%result)
            es_client.indices.open(index=es_index_name)
    else:
        es_client.indices.create(
            index=es_index_name,
            settings=el_config["settings"],
            mappings=el_config["mappings"],
            ignore=400
        )
    mapping = es_client.indices.get_mapping(index=es_index_name)
    print('Mapping: %s'%mapping)
 

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
