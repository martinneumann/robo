#!/usr/bin/env python

import sys, socket, struct

def main():                                                                     
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                    
    server_address = ("192.168.0.101", 9000)                                    
    print >> sys.stderr, "starting on %s port %s" % server_address              
    sock.bind(server_address)                                                   
    # sock.setblocking(False)                                                   
    sock.listen(1)                                                              
    while True:                                                                 
        # Wait for a connection                                                 
        print >>sys.stderr, 'waiting for a connection'                          
        connection, client_address = sock.accept()                              
                                                                                
        try:                                                                    
            print >> sys.stderr, "connection from", client_address              
            data = connection.recv(256)                                        
            print(data)
            # connection.sendall("1A1B2")                                         
            # print >> sys.stderr, "received %s" % data                         
            # if data:                                                          
            #    print >> sys.stderr, "sending data to client"                  
            #    connection.sendall(data)                                       
            # else:                                                             
            #    print >> sys.stderr, "no more data from", client_address       
            #    break                                                          
        finally:                                                                
           # connection.close()
           print("finally")

if __name__ == '__main__':main()                                                
