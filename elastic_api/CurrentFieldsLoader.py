from AbstractLoader import AbstractLoader
import parse_date


class CurrentFieldsLoader(AbstractLoader):
    """
    This Laoder makes a query to on_going_patient_index and returns all fields specified by set_fields()
    """
    def set_fields(self, fields):
        """
        :param fields: list of fields to return from load_value. example: ["CareContactId", "Locations"]
        """
        self.fields = fields

    def load_value(self, start_time, interval_unused):
        return self.client.search(
            index="on_going_patient_index",
            body=
            {
                "size": 10000,
                "fields": self.fields,
                "query": {
                    "match_all": {}
                }
            }
        )
