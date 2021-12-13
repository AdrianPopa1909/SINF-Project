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


if __name__ == '__main__':
    while not es_client.ping():
        print('elastic search db not responfing')
        time.sleep(5)
    print('elastic search db is up')

    mapping_file = open("elastic_seach_mapping.json", "r")
    mapping = json.load(mapping_file)

    index_name = "sinf_index"
    response = es_client.indices.create(
        index=index_name,
        body=mapping,
        ignore=400
    )
    print('Creating the elastic search index. Status %s'%response)

    test_entry = dict()
    test_entry['test_column'] = 'test_1234'
    test_entry['number_column'] = 5678
    test_entry['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    json_data = json.dumps(test_entry)
    index = 0
    es_client.index(index=index_name, id=index, body=json_data)
    index = index + 1

    app.run(host='0.0.0.0', port=5000, debug=True)
