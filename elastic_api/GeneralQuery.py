import os
from elasticsearch import Elasticsearch
import parse_date


class GeneralQuery:
    def __init__(self):
        file_name = os.path.join(os.path.dirname(__file__), 'elasticIP.txt')
        with open(file_name) as f:
            elastic = f.readline()
        self.client = Elasticsearch(elastic)

    def query(self, index, body):
        return self.client.search(index=index, body=body)

    def get_patients_of_team(self, team):
        """
        Queries the database for all patients in the given team
        :param team: the team to search for
        :return: all patients currently under the given team, returned as an array
        """
        index = "on_going_patient_index"
        body = {
            "size": 10000,
            "query": {
                "match": {"Team": team}
            }
        }
        query = self.query(index=index, body=body)
        results = query["hits"]["hits"]
        patients = []
        for result in results:
            patients.append(result["_source"])
        return patients

    def get_all_patients(self):
        """
        :return: array containg all patients currently at the emergency room.
        """
        index = "on_going_patient_index"
        body = {
            "size": 10000,
            "query": {
                "match_all": {}
            }
        }
        query = self.query(index=index, body=body)
        results = query["hits"]["hits"]
        patients = []
        for result in results:
            patients.append(result["_source"])
        return patients


    def get_all_finished_patients(self):
        """
        :return: array containg all patients currently at the emergency room.
        """
        index = "finished_patient_index"

        body = {
            "size": 10000,
            "query": {
                "match_all": {}
            }
        }
        query = self.query(index=index, body=body)
        results = query["hits"]["hits"]
        patients = []
        for result in results:
            patients.append(result["_source"])
        return patients

