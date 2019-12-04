import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
import socket
import sys


def startServer():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created!")

    port = 1234

    enabled = True

    while enabled:
        try:
            #Bind socket to localhost under port defined above
            serverSocket.bind(('', port))
        except socket.error as msg:
            print("Bind failed. Error: " + str(msg))
            sys.exit()
        print("Socket bind complete")

        #Start listening on socket
        # 2 connections kept waiting if server busy. 3rd socket will be refused
        serverSocket.listen(2)
        print("Socket now listening")

        # Establish the connection
        # Accept all incoming connections
        connectionSocket, addr = serverSocket.accept()
        print("Incoming Source address: " + str(addr))

        try:
            #Receive message from the socket
            #1024 = max size in bits to be received at once
            message = connectionSocket.recv(1024)
            print("Message: " + str(message))

            # Close connectionSocket
            connectionSocket.close()
            print("Connection closed!")

            if message == "quit":
                enabled = false

        except IOError:
            # Send response message for invalid file
            connectionSocket.close()



# Returns a list of files inside the "files" directory
def listFiles():
    data_folder = Path("files")
    print("Getting files in: " + str(data_folder))
    files = [f for f in listdir(str(data_folder)) if isfile(join(str(data_folder), f))]
    return files


startServer()
#print(listFiles())
