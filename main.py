#/usr/bin/python3
import socket
import sys
import logging
import queue

#from ComunicationServer import ComunicationServer
from RadarPlot import RadarPlot
from MessageParser import MessageParser

DataQueue = queue.Queue()

Parser = MessageParser(DataQueue)
#Parser.start()
Parser.run()

#server = ComunicationServer(DataQueue)
#server.start()

Radar = RadarPlot(Parser.GetSonarQueue())
Radar.Start()
