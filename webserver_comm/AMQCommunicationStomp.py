import stomp
import json

from webserver_comm import amq_config


class AMQCommunicationStomp:
    """
    This class connects to an activeMQ instance and sends messages to it on /topic/webserver_package. It will need a
    proper ./amq_config to work.
    """
    def __init__(self):
        self.encoder = json.JSONEncoder()

        login = amq_config.config()["login"]
        passcode = amq_config.config()["password"]
        address = amq_config.config()["ip"]
        port = amq_config.config()["port"]
        self.topic = '/topic/webserver_package'
        print "AMQ_Communication.interface connecting to: \naddress: "+address +"port: "+port+"\nlogin: "+login +"passcode: "+passcode
        self.c = stomp.Connection([(address, port)])
        # c.set_listener('', PrintingListener())
        self.c.start()
        self.c.connect(login, passcode, wait=True)


    def send_package(self, data_type, data):
        package = self.encoder.encode({
            "type": data_type,
            "data": data
        })
        self.c.send(self.topic, package)
        print data_type + "package sent: \n" + package + "\n\n"

