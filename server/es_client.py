from elasticsearch import Elasticsearch
from flask import request
import time
import json
from datetime import datetime


class ESClient(object):
    def __init__(self):
        self.index_name = "sinf_index"
        self.index = 0
        self.client = None

    def initDB(self):
        self.client = Elasticsearch(['http://elastic_search:9200/'], verify_certs=True)
        
        while not self.client.ping():
            print('elastic search db not responfing')
            time.sleep(5)
        print('elastic search db is up')

        es_config_file = open("elastic_seach_mapping.json", "r")
        es_config = json.load(es_config_file)

        exists = self.client.indices.exists(index=self.index_name)
        if exists:
            result = self.client.indices.put_mapping(index=self.index_name, body=es_config["mappings"])
            print('Updating mapping: %s'%result)
            self.client.indices.open(index=self.index_name)
        else:
            self.client.indices.create(
                index=self.index_name,
                settings=es_config["settings"],
                mappings=es_config["mappings"],
                ignore=400
            )
        mapping = self.client.indices.get_mapping(index=self.index_name)
        print('Mapping: %s'%mapping)

    def addEntry(self, req, status):
        entry = dict()
        entry['auth'] = req.headers.get("Authorization")
        entry['method'] = req.method
        entry['path'] = req.path
        entry['query_arguments'] = " ".join([x + "=" + y for x, y in req.args.items()])
        entry['response_status'] = status
        entry['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print("New entry: %s"%entry)

        json_data = json.dumps(entry)
        result = self.client.index(index=self.index_name, id=self.index, document=json_data)
        print("Updating the client index %s"%result)

        self.index = self.index + 1

    def addEntryAuth(self, req, args, auth_token, status):
        entry = dict()
        entry['auth'] = auth_token
        entry['method'] = req.method
        entry['path'] = req.path
        entry['query_arguments'] = args
        entry['response_status'] = status
        entry['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print("New entry: %s"%entry)

        json_data = json.dumps(entry)
        result = self.client.index(index=self.index_name, id=self.index, document=json_data)
        print("Updating the client index %s"%result)

        self.index = self.index + 1
    
    def addEntryJson(self, req, args, status):
        entry = dict()
        entry['auth'] = req.headers.get("Authorization")
        entry['method'] = req.method
        entry['path'] = req.path
        entry['query_arguments'] = " ".join([x + "=" + str(args[x]) for x in args])
        entry['response_status'] = status
        entry['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print("New entry: %s"%entry)

        json_data = json.dumps(entry)
        result = self.client.index(index=self.index_name, id=self.index, document=json_data)
        print("Updating the client index %s"%result)

        self.index = self.index + 1
  
es_client = ESClient()