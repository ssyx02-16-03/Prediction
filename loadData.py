from elasticsearch import Elasticsearch
client = Elasticsearch()

response = client.search(
    index="akutenpatients",
    body={
  "size": 0,
  "query": {
    "filtered": {
      "query": {
        "query_string": {
          "query": "*"
        }
      },
      "filter": {
        "bool": {
          "must": [
            {
              "range": {
                "initial.CareContactRegistrationTime": {
                  "gte": 1438552800000,
                  "lte": 1439157600000,
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
        "field": "start",
        "interval": "1h",
        "time_zone": "Europe/Berlin",
        "min_doc_count": 1,
        "extended_bounds": {
          "min": 1438552800000,
          "max": 1439157600000
        }
      }
    }
  }
}
)

print(response['hits']['total'])
f = open('data.txt','w')
for hit in response['aggregations']['2']['buckets']:
    f.write(str(hit['key']) + " " + str(hit['doc_count']) + "\n")

f.close() 
