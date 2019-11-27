#import socket module

import socket
import sys

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket Created!")
port = 80

try:
    #bind the socket to localhost under port 80
    serverSocket.bind(('', port))
except socket.error as msg:
    print("Bind failed. Error Code: " + str(msg[0]) + "Message: " + msg[1])
    sys.exit()
print("Socket bind complete")

#start listening on the socket
#2 connections are kept waiting if server busy. 3rd socket will be refused
serverSocket.listen(2)
print("Socket now listening")

filename = ""
while filename != "/quit":
#Establish the connection
    #Accept all incoming connections
    connectionSocket, addr = serverSocket.accept()
    print("source address: " + str(addr))

    try:
        #Receive message from the socket
        #1024 is max size in bits to be received at once
        message = connectionSocket.recv(1024)
        print("message = " + str(message))
        #obtain file name carried by HTTP request message
        filename = message.split()[1]
		
        print("filename = " + str(filename))
        f = open(filename[1:])
        outputdata = f.read()
        #Send HTTP response header line to the client/connection socket
        connectionSocket.send(bytes("HTTP/1.1 200 OK\n"))
        #send content of requested file to client
        connectionSocket.send(bytes(outputdata))
        #close connectionSocket
        connectionSocket.close()
        print("Connection closed!")

    except IOError:
        #Send response message for invalid file
        connectionSocket.send(bytes("HTTP/1.1 404 Not Found\n"))
        connectionSocket.close()


serverSocket.close()
print("Socket closed, exiting!")
