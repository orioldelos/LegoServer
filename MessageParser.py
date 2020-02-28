import threading
import logging
import queue 
import paho.mqtt.client as MQTT
import time
import ast

logging.basicConfig( level=logging.INFO,
    format='%(message)s')

#class MessageParser(threading.Thread):
class MessageParser():
    sonarsensorQ = queue.Queue()
    odometryQ = queue.Queue()
    TimeToStop = False

    def __init__(self,messageQueue):
        logging.info("Initializing message parser")
        
        self.messageQ = messageQueue

        self.client = MQTT.Client(transport="tcp")
        self.client.on_connect = self.on_connect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.ProcessMessage
        self.client.on_disconnect = self.on_disconnect
        self.client.connect("192.168.59.76", 1883)

        threading.Thread.__init__(self)

    def ProcessMessage(self, client, userdata, msg):
        logging.info("Message received from broker:" +msg.payload.decode())
        Switch = {'robot/sonar': self.PutInSonarQueue, "robot/odo": self.PutInOdometryQueue}
        payloadasobject = ast.literal_eval(msg.payload.decode())
        Switch[msg.topic](payloadasobject)

    def on_connect(self, client, userdata, flags, rc):
        logging.info("Broker Connected with result code "+str(rc))  
        subs = client.subscribe("robot/#")
        logging.info("Subscriptionresult:" + str(subs[0]))

    def run(self):
        #while not self.TimeToStop:
            #self.client.loop_forever()
            self.client.loop_start()
        #self.client.loop_stop()

 
    def on_subscribe(self, client, userdata, mid, granted_qos):
        logging.info("Subscription :" +str(mid)+" "+str(granted_qos))

    def on_disconnect(self, ):
        logging.info("Disconnected")
    
    def PutInSonarQueue(self,message):
        self.sonarsensorQ.put(message)
        
    def PutInOdometryQueue(self,message):
        self.odometryQ.put(message)
    
    def GetSonarQueue(self):
        return self.sonarsensorQ
    def GetOdometryQueue(self):
        return self.odometryQ
