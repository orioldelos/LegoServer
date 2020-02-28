import socket
import sys
import logging
import threading
import ast
from asyncio import Queue


logging.basicConfig( level=logging.INFO,
    format='%(message)s')

class ComunicationServer(threading.Thread):
    def __init__(self,dataSourceQueue):
        logging.info("Initializing comunication server")
        print("Initializing comunication server")

        self.dataqueue = dataSourceQueue
        self.timeToStop = False

        threading.Thread.__init__(self)


    def run(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = ('192.168.59.76', 9999)
        #print >>sys.stderr, 'starting up on %s port %s' % server_address
        logging.debug("Starting up on %s port %sd" % server_address)
        sock.bind(server_address)

        # Listen for incoming connections
        sock.listen(1)
        while not self.timeToStop:
            # Wait for a connection
            #print >>sys.stderr, 'waiting for a connection'
            logging.debug('Waiting for a connection')
            connection, client_address = sock.accept()
            stream=''

            try:
                #print >>sys.stderr, 'connection from', client_address
                logging.debug('connection from:' + str(client_address))

                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(16)
                    #print >>sys.stderr, 'received "%s"' % data
                    if data:
                        datastring = data.decode()
                        for char in datastring:
                            if char == '{':
                                stream = char
                            else:
                                if char == '}':
                                    stream += char
                                    logging.debug(stream)
                                    # We must create the object and push it to the queue
                                    colection = ast.literal_eval(stream)
                                    self.dataqueue.put(colection)
                                else:
                                    stream += char
                            
                    else:
                        #print >>sys.stderr, 'no more data from', client_address
                        logging.debug('no more data from:' + str(client_address))
                        break
                    
            finally:
                # Clean up the connection
                connection.close()

    def Stop(self):
        logging.debug("Stoping Comunications Server")
        self.timeToStop=True