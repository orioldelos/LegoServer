import logging
import time

import paho.mqtt.client as MQTT


class DataSender():
    def __init__(self,SenderID):
        self.client = MQTT.Client(SenderID)
        self.EstablishConnection()
      
    def EstablishConnection(self):
        logging.info("Establishing connection with broker")
        self.client.on_connect = self.OnConnect
        self.client.connect("192.168.59.76")
        
    def OnConnect(self,client, userdata, flags, rc):
        logging.info("Data Sender Connected to Broker")

    def SendToServer(self,topico,Data):
        logging.info("Sending data to broker")
        self.client.publish(topico, str(Data))
        


    