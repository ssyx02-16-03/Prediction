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
                  "lte": 1439262000000,
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
        "interval": "30m",
        "time_zone": "Europe/Berlin",
        "min_doc_count": 1,
        "extended_bounds": {
          "min": 1438570800000,
          "max": 1439262000000
        }
      },
      "aggs": {
        "3": {
          "avg": {
            "field": "totalTime"
          }
        }
      }
    }
  }
}
)

print(response['hits']['total'])
x = []
y = []
count = 0
avg = 0
for hit in response['aggregations']['2']['buckets']:
    time = hit['key_as_string'][11:16]
    x.append(int(time[:-3])*60+int(time[-2:]))

    count = hit['doc_count']
    avg = hit['3']['value']
    y.append(count*avg)


import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

x_plot = np.linspace(0, 1440, 100)

# create matrix versions of these arrays
x_arr = np.asarray(x)
X = x_arr[:, np.newaxis]
X_plot = x_plot[:, np.newaxis]

plt.scatter(x, y, label="training points")

for degree in [3, 4, 5, 6]:
    model = make_pipeline(PolynomialFeatures(degree), Ridge())
    model.fit(X, y)
    y_plot = model.predict(X_plot)
    plt.plot(x_plot, y_plot, label="degree %d" % degree)

plt.legend(loc='upper left')

plt.show()
