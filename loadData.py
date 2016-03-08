# coding=utf-8
from elasticsearch import Elasticsearch
import numpy as np
import json

with open("elasticIP.txt") as f:
  elastic = f.readline()
client = Elasticsearch(elastic)

response = client.search(
    index="*",
    body={
      "size": 0,
      "query": {
        "filtered": {
          "query": {
            "query_string": {
              "analyze_wildcard": True,
              "query": "*"
            }
          },
          "filter": {
            "bool": {
              "must": [
                {
                  "range": {
                    "VisitRegistrationTime": {
                      "gte": 1457046000000,
                      "lte": 1457391600000,
                      "format": "epoch_millis"
                    }
                  }
                }
              ],
              "must_not": []
            }
          }
        }
      },
      "aggs": {
        "2": {
          "date_histogram": {
            "field": "VisitRegistrationTime",
            "interval": "1h",
            "time_zone": "Europe/Berlin",
            "min_doc_count": 1,
            "extended_bounds": {
              "min": 1457046000000,
              "max": 1457391600000
            }
          }
        }
      }
    }
)


print(response['hits']['total'])
x_t = []
y_t = []
tx_t = []
ty_t = []
count = 0
for hit in response['aggregations']['2']['buckets']:
    time = hit['key_as_string'][11:16]
    count = hit['doc_count']
    if(hit['key_as_string'][9:10]!="7"):
        x_t.append(int(time[:-3])*60+int(time[-2:]))
        y_t.append(count)
    else:
        tx_t.append(int(time[:-3])*60+int(time[-2:]))
        ty_t.append(count)


# training data
points = []
for i in np.arange(len(x_t)):
    points.append({'time': x_t[i], 'count': y_t[i]})

data = {'points': points}

with file('training.json', 'w') as f1:
    json.dump(data, f1)
    f1.close()

# test data
points = []
for i in np.arange(len(tx_t)):
    points.append({'time': tx_t[i], 'count': ty_t[i]})

data = {'points': points}

with file('test.json', 'w') as f2:
    json.dump(data, f2)
    f2.close()
