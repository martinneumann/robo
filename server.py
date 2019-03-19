#!/usr/bin/env python

import cv2                                                                      
import numpy as np                                                              
from matplotlib import pyplot as plt                                            
import sys                                                                      
import socket                                                                   
import struct                                                                   
import atexit
from collections import defaultdict
import select

# server the robot client program and the business logic client connect to

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                    
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = ("192.168.0.101", 9000)                                    
print("connecting to server, address is: " + str(server_address))           
sock.bind(server_address)                                                       
# sock.connect(server_address)                                                
sock.listen(1)

inputs = [sock]
outputs = []
message_queues = {}

client_requests = defaultdict(int)

connections = []

def exit_handler():
    for connection in connections:
        print("exiting program, closing connection")
        connection[0].close()

atexit.register(exit_handler)

# simple server: client 1 connects, then client 2
# server sends messages 1/2/1/2 (request/response)

while len(connections) < 2:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    connections.append([connection, client_address])
    print("client connected: " + str(client_address))
    client_requests[client_address[0]] += 1

print("all clients connected, starting routine...")

while True:                                                                   
    data = connections[0][0].recv(255)
    print("received " + str(data) + " from " + str(connections[0][1]))
    message = data
    print("sending " + str(message) + " to " + str(connections[1][1]))
    connections[1][0].sendall(message)
    data = connections[1][0].recv(255)
    print("received " + str(data) + " from " + str(connections[1][1]))
    message = data
    print("sending " + str(message) + " to " + str(connections[0][1]))
    connections[0][0].sendall(message)
    # newinput = raw_input("enter next message: ")                     
    # message = newinput                                                
    # if(newinput == 'q'):
    #   print("closing connection")
    #   connection.close()
    # for client in connections:
    #    client[0].sendall(message)                                                   
    #    print >>sys.stderr, 'sending "%s"' % message                            
