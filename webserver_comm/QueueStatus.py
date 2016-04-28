# coding=utf-8
import time

from PatientsFlows.QueueTimeGraphs import QueueTimeGraphs
from elastic_api.TimeToEventConditionalLoader import TimeToEventConditionalLoader
from elastic_api.TimeToEventLoader import TimeToEventLoader
import PatientsFlows.UsePersistenModel as UsePersistentModel
ONE_HOUR_MILLISECONDS = 60 * 60 * 1000



class QueueStatus:

    def __init__(self):
        self.GRAPH_START_TIME = 10  # hours before now
        self.GRAPH_END_TIME = 2

        now = int(time.time()) * 1000

        loader_start_time = now - ONE_HOUR_MILLISECONDS * 24
        loader_end_time = now
        graph_start_time = now - ONE_HOUR_MILLISECONDS * self.GRAPH_START_TIME
        graph_end_time = now

        loader = TimeToEventLoader("0001-01-01 00:00", "0001-01-01 00:00", 0)
        # set times by means of fulhack
        loader.end_time = loader_end_time
        loader.start_time = loader_start_time

        # actual line data
        self.ttt_x, self.ttt_y, self.ttt_pred_x, self.ttt_pred_y = UsePersistentModel.predict_now(loader_start_time, loader_end_time, "TimeToTriage")
        self.ttl_x, self.ttl_y, self.ttl_pred_x, self.ttl_pred_y = UsePersistentModel.predict_now(loader_start_time, loader_end_time, "TimeToDoctor")
        self.tvt_x, self.tvt_y, self.tvt_pred_x, self.tvt_pred_y = UsePersistentModel.predict_now(loader_start_time, loader_end_time, "TotalTime")
        self.ttk_x, self.ttk_y, self.ttk_pred_x, self.ttk_pred_y = UsePersistentModel.predict_now(loader_start_time, loader_end_time, "TimeToFinished")

        # data points for the circles
        matched_loader = TimeToEventConditionalLoader(loader_start_time, loader_end_time, 0)

        self.ttk_surgery, self.ttl_surgery, self.tvt_surgery = self.get_points(matched_loader, "default", ["NAKKI"], graph_start_time, graph_end_time)
        self.ttk_ort, self.ttl_ort, self.tvt_ort = self.get_points(matched_loader, "default", ["NAKOR"], graph_start_time, graph_end_time)
        self.ttk_jour, self.ttl_jour, self.tvt_jour = self.get_points(matched_loader, "default", [u"NAKÖN", "NAKBA"], graph_start_time, graph_end_time)
        self.ttk_blue_med, self.ttl_blue_med, self.tvt_blue_med = self.get_points(matched_loader, "medicineBlue", ["NAKME"], graph_start_time, graph_end_time)
        self.ttk_yellow_med, self.ttl_yellow_med, self.tvt_yellow_med = self.get_points(matched_loader, "medicineYellow", ["NAKME"], graph_start_time, graph_end_time)

    def get_line_graph_data(self):
        return {
            "time_axis":{
                "start": -self.GRAPH_START_TIME,
                "end": self.GRAPH_END_TIME
            },
            "ttt": self.jsonize_ttt(self.ttt_x, self.ttt_y, self.ttt_pred_x, self.ttt_pred_y),
            "ttk": self.jsonize_tvt_ttl_ttk(self.ttk_x, self.ttk_y, self.ttk_pred_x, self.ttk_pred_y,
                                        blue=self.ttk_blue_med,
                                        yellow=self.ttk_yellow_med,
                                        surgery=self.ttk_surgery,
                                        orthopedia=self.ttk_ort,
                                        jour=self.ttk_jour),
            "ttl": self.jsonize_tvt_ttl_ttk(self.ttl_x, self.ttl_y, self.ttl_pred_x, self.ttl_pred_y,
                                        blue=self.ttl_blue_med,
                                        yellow=self.ttl_yellow_med,
                                        surgery=self.ttl_surgery,
                                        orthopedia=self.ttl_ort,
                                        jour=self.ttl_jour),
            "tvt": self.jsonize_tvt_ttl_ttk(self.tvt_x, self.tvt_y, self.tvt_pred_x, self.tvt_pred_y,
                                        blue=self.tvt_blue_med,
                                        yellow=self.tvt_yellow_med,
                                        surgery=self.tvt_surgery,
                                        orthopedia=self.tvt_ort,
                                        jour=self.tvt_jour)
        }

    def get_vector(self, loader, start_time, end_time):

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

        return trend

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

    def get_points(self, loader, torg, teams, start_time, end_time):
        loader.set_teams(teams)
        loader.set_torg(torg)

        loader.set_event_name("TimeToFinished")
        ttk = self.get_vector(loader, start_time, end_time)[-1]["y"]

        loader.set_search_removed()
        tvt = self.get_vector(loader, start_time, end_time)[-1]["y"]

        loader.set_search_doctor()
        ttl = self.get_vector(loader, start_time, end_time)[-1]["y"]
        return ttk, ttl, tvt

    def jsonize_tvt_ttl_ttk(self, ttv_x, ttv_y, ttv_pred_x, ttv_pred_y, blue, yellow, surgery, orthopedia, jour):
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
