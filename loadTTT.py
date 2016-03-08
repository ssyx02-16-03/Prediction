from elasticsearch import Elasticsearch
import numpy as np
import json

with open("elasticIP.txt") as f:
  elastic = f.readline()
client = Elasticsearch(elastic)

response = client.search(
    index="*",
    body =
    {
        "size": 1000,
        "query": {
            "match_all" : { }
        },
        "filter": {
            "and": [
                {
                    "range": {
                        "VisitRegistrationTime": {
                            "gte": "2016-03-06 00:00:00",
                            "lte": "2016-03-07 00:00:00",
                            "format": "yyyy-MM-dd HH:mm:ss"
                        }
                    }
                },
                {
                    "range": {
                        "TimeToTriage": {
                            "gte": 0
                        }
                    }
                }
            ]
        }
    }
)

print(response['hits']['total'])

# print response['hits']['hits'][1]['_source']['TimeToTriage']

triage_times = [];

for hit in response['hits']['hits']:
    triage_times.append(hit['_source']['TimeToTriage'])

print triage_times