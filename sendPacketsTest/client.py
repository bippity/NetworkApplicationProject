import socket

# Sends message to Server
def sendMessage():
    print("Sending message to server")
    msg = "Hello Server!"

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverIP = "10.0.0.2"
    port = 1234
    clientSocket.connect((serverIP, port))
    clientSocket.sendall(msg)
    
    receivedData = clientSocket.recv(1024)
    clientSocket.close()
    
    print "Received:", str(receivedData)
    
sendMessage()