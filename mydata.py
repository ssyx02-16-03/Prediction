# coding=utf-8
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
                                        "lte": 1458039762969,
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
                    "interval": "5h",
                    "time_zone": "Europe/Berlin",
                    "min_doc_count": 1,
                    "extended_bounds": {
                        "min": 1457046000000,
                        "max": 1458039762969
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
avg = 0
for hit in response['aggregations']['2']['buckets']:
    #avg = hit['1']['value']
    #if(avg is not None):
        time = hit['key_as_string'][11:16]
        count = hit['doc_count']
        if(hit['key_as_string'][9:10]!="7"):
            x_t.append(int(time[:-3])*60+int(time[-2:]))
            y_t.append(count)
        else:
            tx_t.append(int(time[:-3])*60+int(time[-2:]))
            ty_t.append(count)


import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.externals import joblib


x_plot = np.linspace(0, 1440, 100)

# create matrix versions of these arrays
y = np.asarray(y_t)
x = np.asarray(x_t)
tx = np.asarray(tx_t)
ty = np.asarray(ty_t)
X = x[:, np.newaxis]
TX = tx[:, np.newaxis]
X_plot = x_plot[:, np.newaxis]

plt.scatter(x, y, label="training points")
plt.scatter(tx, ty, label="test points", c='g')

print X.shape
for degree in [3, 4, 5]:
    model = make_pipeline(PolynomialFeatures(degree), Ridge())
    model.fit(X, y)
    print model.score(TX, ty)
    y_plot = model.predict(X_plot)
    plt.plot(x_plot, y_plot, label="degree %d" % degree)
plt.legend(loc='upper left')

plt.show()