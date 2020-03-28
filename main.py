#/usr/bin/python3
import socket
import sys
import logging
import queue as Queue

#from ComunicationServer import ComunicationServer
from RadarPlot import RadarPlot
from MessageParser import MessageParser
import DriveCommander

DataQueue = Queue.Queue()
Commander = DriveCommander.DriveCommander()
Commander.start()
Parser = MessageParser(DataQueue)
#Parser.start()
Parser.run()

#server = ComunicationServer(DataQueue)
#server.start()

Radar = RadarPlot(Parser.GetSonarQueue())
Radar.Start()


