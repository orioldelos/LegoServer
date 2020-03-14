import logging
import time

import paho.mqtt.client as MQTT


class DataSender():
    def __init__(self,SenderID):
        #logging.debug("DataSender Initializing")
        #self.client = MQTT.Client(SenderID, "192.168.59.76", port=1883)
        self.client = MQTT.Client(SenderID)
        self.EstablishConnection()
      
    def EstablishConnection(self):
        logging.info("Establishing connection with broker")
        #client.set_callback(sub_cb) 
        self.client.on_connect = self.OnConnect
        self.client.connect("192.168.59.76")
        #client.subscribe(topic="youraccount/feeds/lights")
        

    def OnConnect(self,client, userdata, flags, rc):
        logging.info("Connected to Broker")


    def SendToServer(self,topico,Data):
        logging.info("Sending data to broker")
        self.client.publish(topico, str(Data))
        


    