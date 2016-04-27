# coding=utf-8
import time

from PatientsFlows.QueueTimeGraphs import QueueTimeGraphs
from elastic_api.TimeToEventConditionalLoader import TimeToEventConditionalLoader
from elastic_api.TimeToEventLoader import TimeToEventLoader
import numpy as np
import PatientsFlows.UsePersistenModel as UsePersistentModel
ONE_HOUR_MILLISECONDS = 60 * 60 * 1000


class QueueStatus:
    def __init__(self):
        now = int(time.time()) * 1000

        loader_start_time = now - ONE_HOUR_MILLISECONDS * 24
        loader_end_time = now
        graph_start_time = now - ONE_HOUR_MILLISECONDS * 12
        graph_end_time = now

        loader = TimeToEventLoader("0001-01-01 00:00", "0001-01-01 00:00", 0)
        # set times by means of fulhack
        loader.end_time = loader_end_time
        loader.start_time = loader_start_time

        # actual line data
        loader.set_search_triage()
        self.ttt_x, self.ttt_y, self.ttt_pred_x, self.ttt_pred_y = UsePersistentModel.predict_now(loader_start_time, loader_end_time, "TimeToTriage")
        self.ttd_x, self.ttd_y, self.ttd_pred_x, self.ttd_pred_y = UsePersistentModel.predict_now(loader_start_time, loader_end_time, "TimeToDoctor")
        self.ttk_x, self.ttk_y, self.ttk_pred_x, self.ttk_pred_y = UsePersistentModel.predict_now(loader_start_time, loader_end_time, "TotalTime")

        # data points for the circles
        matched_loader = TimeToEventConditionalLoader("0001-01-01 00:00", "0001-01-01 00:00", 0)
        matched_loader.end_time = loader_start_time
        matched_loader.start_time = loader_end_time

        self.ttk_surgery, self.ttd_surgery = self.get_points(matched_loader, "default", ["NAKKI"], graph_start_time, graph_end_time)
        self.ttk_ort, self.ttd_ort = self.get_points(matched_loader, "default", ["NAKOR"], graph_start_time, graph_end_time)
        self.ttk_jour, self.ttd_jour = self.get_points(matched_loader, "default", [u"NAKÖN", "NAKBA"], graph_start_time, graph_end_time)
        self.ttk_blue_med, self.ttd_blue_med = self.get_points(matched_loader, "medicineBlue", ["NAKME"], graph_start_time, graph_end_time)
        self.ttk_yellow_med, self.ttd_yellow_med = self.get_points(matched_loader, "medicineYellow", ["NAKME"], graph_start_time, graph_end_time)

    def get_line_graph_data(self):
        return {
            "ttt": self.jsonize_ttt(self.ttt_x, self.ttt_y, self.ttt_pred_x, self.ttt_pred_y),
            "ttd": self.jsonize_ttd_ttk(self.ttd_x, self.ttd_y, self.ttd_pred_x, self.ttd_pred_y,
                                    blue=self.ttd_blue_med,
                                    yellow=self.ttd_yellow_med,
                                    surgery=self.ttd_surgery,
                                    orthopedia=self.ttd_ort,
                                    jour=self.ttd_jour),
            "ttk": self.jsonize_ttd_ttk(self.ttk_x, self.ttk_y, self.ttk_pred_x, self.ttk_pred_y,
                                    blue=self.ttk_blue_med,
                                    yellow=self.ttk_yellow_med,
                                    surgery=self.ttk_surgery,
                                    orthopedia=self.ttk_ort,
                                    jour=self.ttk_jour)
        }

    def get_vectors(self, loader, start_time, end_time):  # TODO add prediction part
        queue_time_graphs = QueueTimeGraphs(loader)
        x_axis, y_axis = queue_time_graphs.moving_average()

        # find start and end indices
        length = len(x_axis)
        i = 0
        while i < length and x_axis[i] < start_time:
            i += 1
        start_index = i

        while i < length and x_axis[i] < end_time:
            i += 1
        end_index = i

        # make trend graph data
        trend = []
        for i in range(start_index, end_index):
            trend.append({
                "x": x_axis[i] - start_time,
                "y": y_axis[i]
            })

        # make prediction graph data; silly placeholder data for now
        prediction = []
        for i in range(0, 60):
            prediction.append({
                "x": 800000,
                "y": 50
            })


        return {
            "trend": trend,
            "prediction": prediction
        }


    def jsonize_ttt(self, ttv_x, ttv_y,ttv_pred_x, ttv_pred_y ):
        trend = []
        prediction = []

        for i in range(0, len(ttv_x)):
            trend.append({
                "x": ttv_x[i][0],
                "y": ttv_y[i]
            })

        for i in range(0, len(ttv_pred_x)):
            prediction.append({
                "x": ttv_pred_x[i],
                "y": ttv_pred_y[i]
            })

        return {
            "trend": trend,
            "prediction": prediction,
            "current_value": prediction[0]
        }


    def get_points(self, loader, teams, torg, start_time, end_time):
        loader.set_teams(teams)
        loader.set_torg(torg)

        loader.set_search_removed()
        ttk = self.get_vectors(loader, start_time, end_time)["trend"]

        loader.set_search_doctor()
        ttd = self.get_vectors(loader, start_time, end_time)["trend"]
        return ttk, ttd

    def jsonize_ttd_ttk(self, ttv_x, ttv_y, ttv_pred_x, ttv_pred_y, blue, yellow, surgery, orthopedia, jour):
        trend = []
        prediction = []

        for i in range(0, len(ttv_x)):
            trend.append({
                "x": ttv_x[i][0],
                "y": ttv_y[i]
            })

        for i in range(0, len(ttv_pred_x)):
            prediction.append({
                "x": ttv_pred_x[i],
                "y": ttv_pred_y[i]
            })

        list = [blue, yellow, surgery, orthopedia, jour]
        list.sort()
        median = list[2]

        return {
            "trend": trend,
            "prediction": prediction,
            "times": {
                "Blue": blue,
                "Gul": yellow,
                "Ki": surgery,
                "Ort": orthopedia,
                "Jour": jour,
                "median": median
            }
        }
