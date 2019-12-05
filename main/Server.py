
import base64
import json
import os
from os import listdir
from os.path import isfile, join
import socket
import sys
import utils
from utils import *


def startServer():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created!")

    port = 1234
    
    try:
        #Bind socket to localhost under defined port
        serverSocket.bind(('', port))
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
                print("Files: " + str(files))
                #Convert list to JSON to send across socket
                data = json.dumps({"Content": files})
                connectionSocket.sendall(data)
                
            elif type == MessageTypes.EXIT:
                enabled = False
                data = json.dumps({"Content": "[SERVER] shutting down"})
                connectionSocket.sendall(data)

            
            # Close connectionSocket            
            connectionSocket.close()
            print("Connection closed!")
                
        except IOError:
            # Send response message for invalid file
            print("IOError detected!")
            connectionSocket.close()
            
    serverSocket.shutdown(socket.SHUT_RDWR)
    serverSocket.close()
    print("Exiting...")
    
    
# Returns a list of files inside the "files" directory
def listFiles():
    data_folder = os.path.normpath("files")
    print("Getting files in: " + data_folder)
    files = [f for f in listdir(data_folder) if isfile(join(data_folder, f))]
    files.sort()
    return files


# Encode the data and send it
def sendFile(connSocket, rawData):
    payload = {}
    payload['content'] = base64.b64encode(rawData)


startServer()
