from elasticsearch import Elasticsearch

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
                  "gte": 1456759721518,
                  "lte": 1457364521518,
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
          "min": 1456759721517,
          "max": 1457364521517
        }
      },
      "aggs": {
        "1": {
          "avg": {
            "field": "TimeToDoctor"
          }
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
    avg = hit['1']['value']
    if(avg is not None):
        time = hit['key_as_string'][11:16]
        count = hit['doc_count']
        x_t.append(int(time[:-3])*60+int(time[-2:]))
        y_t.append(avg)


import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

x_plot = np.linspace(0, 1440, 100)

# create matrix versions of these arrays
y = np.asarray(y_t)
x = np.asarray(x_t)
X = x[:, np.newaxis]
X_plot = x_plot[:, np.newaxis]

plt.scatter(x, y, label="training points")

for degree in [3, 4, 5]:
    model = make_pipeline(PolynomialFeatures(degree), Ridge())
    model.fit(X, y)
    y_plot = model.predict(X_plot)
    plt.plot(x_plot, y_plot, label="degree %d" % degree)

plt.legend(loc='upper left')

#plt.show()

 
from sklearn.svm import SVR
 
# # Fit regression model
svr_rbf = SVR(kernel='rbf', degree=3, C=1e3)
y_rbf = svr_rbf.fit(X, y).predict(X)
plt.hold('on')
plt.plot(X, y_rbf, c='g', label='RBF model')
plt.show()
