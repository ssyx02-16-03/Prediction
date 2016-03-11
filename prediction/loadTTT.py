from elasticsearch import Elasticsearch
import numpy as np
import json

with open("elasticIP.txt") as f:
  elastic = f.readline()
client = Elasticsearch(elastic)

startTime = "2016-03-06 00:00:00"
endTime = "2016-03-07 00:00:00"

response = client.search(
    index="*",
    body=
    {
        "size": 0,
        "query": {
            "match_all" : { }
        },
        "filter": {
            "and": [
                {
                    "range": {
                        "VisitRegistrationTime": {
                            "gte": startTime,
                            "lte": endTime,
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

triage_times = []

for hit in response['hits']['hits']:
    triage_times.append(hit['_source']['TimeToTriage'])

print triage_times