import os
from elasticsearch import Elasticsearch
import parse_date


class GeneralQuery:
    def __init__(self):
        file_name = os.path.join(os.path.dirname(__file__), 'elasticIP.txt')
        with open(file_name) as f:
            elastic = f.readline()
        self.client = Elasticsearch(elastic)

    def query(self, index, body):
        return self.client.search(index=index, body=body)

