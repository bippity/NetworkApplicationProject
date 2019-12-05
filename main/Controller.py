'''
Controller class
Displays the menu to the user
Can request list of files in Server
Tells the Renderer to request a file from the Server
'''

import json
import socket
import sys
import utils
from utils import MessageTypes


serverIP = "10.0.0.2"
rendererIP = ""
port = 1234

def getMenuInput():
    menu = ("===[Network Application]===\n"
            "1) List files in Server.\n"
            "2) Open file.\n"
            "3) Close file.\n"
            "4) Exit.\n")
    while True:
        try:
            inputVal = int(input(menu + "Choose an option: "))
        except ValueError:
            print("Invalid option. Please try again.")
            continue

        if inputVal < 1 or inputVal > 4:
            print("Invalid option. Out of range (1-4).")
        else:
            break

    return inputVal


#Lists server files in a list
def getServerFiles():   
    #Create payload message
    payload = json.dumps({"type": MessageTypes.FETCH})
    data = sendMessage(MessageTypes.FETCH, payload)
    
    #Decode the recieved data from unicode, then Parse data into JSON format
    data = utils.json_loads_byteified(data)
    files = data.get("Content")

    print("List of files in Server:")
    print(str(files))

#Tell renderer to request the specified file via ID from the Server
def openServerFile():
    print("Getting file")


def closeServerFile():
    print("Closing file")
    
    
def sendMessage(type, payload):
    #Create TCP socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Determine what message to send
    #Send fetch request of server files
    if type == MessageTypes.FETCH:
        clientSocket.connect((serverIP, port))
        clientSocket.sendall(payload)
        
    elif type == MessageTypes.EXIT:
        clientSocket.connect((serverIP, port))
        clientSocket.sendall(payload)
        
    data = clientSocket.recv(1024)
    clientSocket.close()
    return data

# Tells Server to shutdown/stop
def closeServer():
    payload = json.dumps({"type": MessageTypes.EXIT})
    data = sendMessage(MessageTypes.EXIT, payload)
    data = utils.json_loads_byteified(data)
    msg = data.get("Content")
    print(str(msg))

# Map inputs to functions
val = int
while val != 4:
    val = getMenuInput()

    if val == 1:
        getServerFiles()
    elif val == 2:
        openServerFile()
    elif val == 3:
        closeServerFile()
    elif val == 4:
        print("Exiting...")
        closeServer()
        sys.exit()
        
    print("\n")
