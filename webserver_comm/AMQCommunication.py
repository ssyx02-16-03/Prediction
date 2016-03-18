from stompest.config import StompConfig
from stompest.sync import Stomp
import json


class AMQCommunication:
    """
    This class connects to an activeMQ instance and sends messages to it on /topic/webserver_package. It will need a
    proper ./amq_config to work.
    """
    def __init__(self):
        self.encoder = json.JSONEncoder()

        with open("amq_config") as file:
            login = file.readline()
            passcode = file.readline()
            address = file.readline()

        print "AMQ_Communication.interface connecting to: \naddress: "+ address +"\nlogin: "+login +"passcode: "+passcode
        config = StompConfig('tcp://'+address, login, passcode)
        self.topic = '/topic/webserver_package'
        self.client = Stomp(config)
        self.client.connect()

    def send_package(self, data_type, data):
        package = self.encoder.encode({
            "type": data_type,
            "data": data
        })
        self.client.send(self.topic, package)
        print "package sent: " + package
