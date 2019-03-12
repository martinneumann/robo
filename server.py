#!/usr/bin/env python

import cv2                                                                      
import numpy as np                                                              
from matplotlib import pyplot as plt                                            
import sys                                                                      
import socket                                                                   
import struct                                                                   
import atexit

# server the robot client program and the business logic client connect to

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                    
server_address = ("192.168.0.101", 9000)                                    
print("connecting to server, address is: " + str(server_address))           
sock.bind(server_address)                                                       
# sock.connect(server_address)                                                
sock.listen(1)
message = '1A1'                                                             


def exit_handler():
    print("exiting program, closing connection")

atexit.register(exit_handler)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    print("client connected")

    while(1):                                                                   
	# Send data                                                             
	connection.sendall(message)                                                   
	print >>sys.stderr, 'sending "%s"' % message                            

	data = connection.recv(255)
	print("received " + str(data))
	newinput = raw_input("enter next message: 1")                     
	message = '1' + newinput                                                
	if(newinput == 'q'):
	    print("closing connection")
	    connection.close()

