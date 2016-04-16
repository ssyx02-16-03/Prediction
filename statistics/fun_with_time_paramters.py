# coding=utf-8
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from elastic_api.GeneralQuery import GeneralQuery

'''
This was an attempt to conduct some statistical analysis on the datasett
'''


def histogramize(x, from_x, to_x, n, xlabel, y_max):
    x_truncated = []
    for val in x:
        if val < to_x:
            x_truncated.append(val)
    x_truncated[-1] = to_x

    plt.hist(x_truncated, n, normed=0, facecolor='green', alpha=0.75)
    plt.axis([from_x, to_x, 0, y_max])
    plt.grid(True)
    plt.xlabel(xlabel)
    plt.ylabel('Probability')

class Team:
    color = {
        u"": {
            "ttt": [],
            "ttl": [],
            "ttk": []
        },
        u"Blå": {
            "ttt": [],
            "ttl": [],
            "ttk": []
        },
        u"Grön": {
            "ttt": [],
            "ttl": [],
            "ttk": []
        },
        u"Gul": {
            "ttt": [],
            "ttl": [],
            "ttk": []
        },
        u"Orange": {
            "ttt": [],
            "ttl": [],
            "ttk": []
        },
        u"Röd": {
            "ttt": [],
            "ttl": [],
            "ttk": []
        }
    }


teams = {
    "nakme": Team(),
    "nakki": Team(),
    "nakor": Team(),
    "nakba": Team(),
    "other": Team()
}

def histogramize_ttx(team, ttx, max_x):
    plt.subplot(411)
    plt.title(ttx)
    histogramize(teams[team].color[u"Grön"][ttx], 0, max_x, 100, "Green", 50)
    plt.subplot(412)
    histogramize(teams[team].color[u"Gul"][ttx], 0, max_x, 100, "Gul", 150)
    plt.subplot(413)
    histogramize(teams[team].color[u"Orange"][ttx], 0, max_x, 100, "Orange", 110)
    plt.subplot(414)
    histogramize(teams[team].color[u"Röd"][ttx], 0, max_x, 100, "Red", 20)




print "searching..."
patients = GeneralQuery().get_all_finished_patients()
print "search complete"

for patient in patients:
    try:
        teams[patient["Team"]].color[patient["Priority"]]["ttt"].append(patient["TimeToTriage"])
        teams[patient["Team"]].color[patient["Priority"]]["ttl"].append(patient["TimeToDoctor"])
        teams[patient["Team"]].color[patient["Priority"]]["ttk"].append(patient["TotalTime"])
    except:
        teams["other"].color[patient["Priority"]]["ttt"].append(patient["TimeToTriage"])
        teams["other"].color[patient["Priority"]]["ttl"].append(patient["TimeToDoctor"])
        teams["other"].color[patient["Priority"]]["ttk"].append(patient["TotalTime"])


# print teams["nakme"].color["Gul"]["ttt"]

#histogramize_ttx("nakme", "ttl", 40000000)
histogramize_ttx("nakme", "ttk", 80000000)


plt.show()








