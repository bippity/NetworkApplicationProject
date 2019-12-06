'''
Renderer class
Retrieves files that the Controller requests from the Server
Displays the file to the user
Needs 2 sockets, for Controller and Server
https://github.com/bippity/NetworkApplicationProject/
'''

import base64
import json
import os
import socket
import sys
import utils
from utils import *

#Start listen server
def startRenderer():
    renderSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #So you won't have to wait for address to timeout
    renderSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Render Socket created!")
    
    try:
        #Bind socket to localhost under defined port
        renderSocket.bind(('', Ports.RENDERER))
        print("Render Socket bind complete")

    except socket.error as msg:
        print("Bind failed. Error: " + str(msg))
        sys.exit()
        
    #Start listening on socket for Controller requests
    # 2 connections kept waiting if server busy. 3rd connection will be refused
    renderSocket.listen(2)
    print("Socket now listening")

    enabled = True
    while enabled:
        # Establish connections
        # Accept all incoming connections
        connectionSocket, addr = renderSocket.accept()
        print("Incoming Source address: " + str(addr))
        
        try:
            # Receive message from the socket
            #1024 = max size in bytes to be received at once
            message = connectionSocket.recv(1024)
            print("Message: " + str(message))
            
            # Decode the message
            message = utils.json_loads_byteified(message)
            type = message.get("type")
            
            if type == MessageTypes.REQUEST:
                # Convert request back to JSON and send to Server
                data = json.dumps(message)
                
                #Create TCP socket
                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sendFileRequest(clientSocket, data)
                
                # Decode the received file
                data = clientSocket.recv(2048)
                clientSocket.close()
                
                payload = utils.json_loads_byteified(data)
                if payload["type"] == MessageTypes.ERROR:
                    print(payload["content"])
                else:            
                    fileName = payload["fileName"]
                    fileData = payload["content"]
                    
                    print("Displaying file: " + fileName)
                    print(fileData)
                
            elif type == MessageTypes.EXIT:
                enabled = False
                data = json.dumps({"content": "[RENDERER] shutting down"})
                connectionSocket.sendall(data)

            
            # Close connectionSocket            
            connectionSocket.close()
            print("Connection closed!")
                
        except IOError as err:
            # Send response message for invalid file
            print("IOError: " + str(err))
            connectionSocket.close()
            
    renderSocket.shutdown(socket.SHUT_RDWR)
    renderSocket.close()
    print("Exiting...")
    
    
# Request a file from Server
def sendFileRequest(clientSocket, payload):
    #Send request of file
    clientSocket.connect((Addresses.SERVER, Ports.SERVER))
    clientSocket.sendall(payload)
    
    
startRenderer()    
    