import stomp
import json


class AMQCommunicationStomp:
    """
    This class connects to an activeMQ instance and sends messages to it on /topic/webserver_package. It will need a
    proper ./amq_config to work.
    """
    def __init__(self, config):
        self.encoder = json.JSONEncoder()

        login = config.readline()
        passcode = config.readline()
        address = config.readline()
        port = config.readline()
        self.topic = '/topic/webserver_package'
        print "AMQ_Communication.interface connecting to: \naddress: "+ address +"\nlogin: "+login +"passcode: "+passcode
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

