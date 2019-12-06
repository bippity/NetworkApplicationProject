'''
Server class
Listens for requests made by the Controller and Renderer
Sends a list of files to Controller
Sends actual files to Renderer
https://github.com/bippity/NetworkApplicationProject/
'''

import json
import os
from os import listdir
from os.path import isfile, join
import socket
import sys
import utils
from utils import *

data_folder = os.path.normpath("files")


#Start listen server
def startServer():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #So you won't have to wait for address to timeout
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket created!")
    
    try:
        #Bind socket to localhost under defined port
        serverSocket.bind(('', Ports.SERVER))
        print("Socket bind complete")
    except socket.error as msg:
        print("Bind failed. Error: " + str(msg))
        sys.exit()
    
    #Start listening on socket
    # 2 connections kept waiting if server busy. 3rd socket will be refused
    serverSocket.listen(2)
    print("Socket now listening")

    enabled = True
    while enabled:
        # Establish connections
        # Accept all incoming connections
        connectionSocket, addr = serverSocket.accept()
        print("Incoming Source address: " + str(addr))
        
        try:
            # Receive message from the socket
            #1024 = max size in bits to be received at once
            message = connectionSocket.recv(1024)
            print("Message: " + str(message))
            
            # Decode the message
            message = utils.json_loads_byteified(message)
            type = message.get("type")
            
            if type == MessageTypes.FETCH:
                files = listFiles()
                #Convert list to JSON to send across socket
                data = json.dumps({"content": files})
                connectionSocket.sendall(data)
                
            elif type == MessageTypes.REQUEST:
                # Obtain file
                fileName = message.get("content")
                sendFile(connectionSocket, fileName)                
                
            elif type == MessageTypes.EXIT:
                enabled = False
                data = json.dumps({"content": "[SERVER] shutting down"})
                connectionSocket.sendall(data)

            
            # Close connectionSocket            
            connectionSocket.close()
            print("Connection closed!")
                
        except IOError as err:
            # Send response message for invalid file
            print("IOError: " + str(err))
            payload = {}
            payload["type"] = MessageTypes.ERROR
            payload["content"] = "File does not exist: " + fileName
            connectionSocket.sendall(json.dumps(payload))
            connectionSocket.close()
            
    serverSocket.shutdown(socket.SHUT_RDWR)
    serverSocket.close()
    print("Exiting...")
    
    
# Returns a list of files inside the "files" directory
def listFiles():
    files = [f for f in listdir(data_folder) if isfile(join(data_folder, f))]
    files.sort()
    return files


# Encode the data and send it
def sendFile(connSocket, fileName):
    #Open file in read-binary
    file = open(join(data_folder, fileName), "rb")
    payload = {}
    payload["type"] = MessageTypes.RESPONSE
    payload["fileName"] = fileName
    payload["content"] = file.read()
    data = json.dumps(payload)
    connSocket.sendall(data)

startServer()
