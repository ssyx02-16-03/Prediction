from elasticsearch import Elasticsearch
import numpy as np
import json

with open("elasticIP.txt") as f:
  elastic = f.readline()
client = Elasticsearch(elastic)

response = client.search(
    index="*",
    body=
{
  "size": 0,
  "query": {
    "filtered": {
      "query": {
        "query_string": {
          "query": "*",
          "analyze_wildcard": True
        }
      },
      "filter": {
        "bool": {
          "must": [
            {
              "range": {
                "VisitRegistrationTime": {
                  "gte": 1457218800000,
                  "lte": 1457305200000,
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
          "min": 1457218800000,
          "max": 1457305200000
        }
      }
    }
  }
}
)


print(response['hits']['total'])
x_t = []
y_t = []
count = 0
avg = 0
for hit in response['aggregations']['2']['buckets']:
    #avg = hit['1']['value']
    #if(avg is not None):
        time = hit['key_as_string'][11:16]
        count = hit['doc_count']
        x_t.append(int(time[:-3])*60+int(time[-2:]))
        y_t.append(count)

points = []

for i in np.arange(len(x_t)):
    points.append({'tid': x_t[i], 'count': y_t[i]})

data = {'points': points}

with file('test.json', 'w') as file:
    json.dump(data, file)
    file.close()