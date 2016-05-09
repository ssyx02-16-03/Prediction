from elasticsearch import Elasticsearch
import os


class ESClient(Elasticsearch):
    """
    Harmless little client to our ES-server
    """
    def __init__(self):
        path_str = '../elastic_api/elasticIP.txt'
        path = os.path.join(os.path.dirname(__file__), path_str)
        with open(path) as file:
            ip = file.readline()
        super(ESClient, self).__init__(ip)
