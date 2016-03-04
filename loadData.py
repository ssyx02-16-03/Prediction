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
                  "gte": 1438570800000,
                  "lte": 1438657200000,
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
          "min": 1438570800000,
          "max": 1438657200000
        }
      }
    }
  }
}
)

print(response['hits']['total'])
f = open('data.txt','w')
x = []
y = []
for hit in response['aggregations']['2']['buckets']:
    x.append(hit['key'])
    y.append(hit['doc_count'])
    f.write(str(hit['key']) + " " + str(hit['doc_count']) + "\n")

f.close() 

import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

x_plot = np.linspace(1438570800000, 1438657200000, 100)

# generate points and keep a subset of them

# create matrix versions of these arrays
x_arr = np.asarray(x)
X = x_arr[:, np.newaxis]
X_plot = x_plot[:, np.newaxis]

plt.scatter(x, y, label="training points")

for degree in [3, 4, 5]:
    model = make_pipeline(PolynomialFeatures(degree), Ridge())
    model.fit(X, y)
    y_plot = model.predict(X_plot)
    plt.plot(x_plot, y_plot, label="degree %d" % degree)

plt.legend(loc='lower left')

plt.show()
