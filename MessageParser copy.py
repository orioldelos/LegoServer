import threading
import logging
import queue import MQTTClient

class MessageParser(threading.Thread):
    sonarsensorQ = queue.Queue()
    odometryQ = queue.Queue()
    TimeToStop = False

    def __init__(self,messageQueue):
        self.messageQ = messageQueue
        threading.Thread.__init__(self)

    def run(self):
        while not self.TimeToStop:
            message = self.messageQ.get()
            Switch = {'ECHO': self.PutInSonarQueue, "ODO": self.PutInOdometryQueue}
            Switch[message['TYPE']](message)

    def PutInSonarQueue(self,message):
        self.sonarsensorQ.put(message)
    
    def PutInOdometryQueue(self,message):
        self.odometryQ.put(message)
    
    def GetSonarQueue(self):
        return self.sonarsensorQ
    def GetOdometryQueue(self):
        return self.odometryQ

    def GetLatestSonarSwipe(self, sonarq):




    
