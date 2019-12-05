'''
Controller class
Displays the menu to the user
Can request list of files in Server
Tells the Renderer to request a file from the Server
'''

import json
import socket
import sys


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


#Lists server files in a numbered list. Don't allow user to freely type the file name.
def getServerFiles():
    #Create TCP socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverIP, port))
    msg = "GIVE ME THE FILES"
    clientSocket.sendall(msg)
    
    data = clientSocket.recv(1024)
    clientSocket.close()
    print("Raw data: " + data)
    #Parse data into JSON format...don't need to decode?
    data = json.loads(data)
    print("Formatted data: " + str(data))
    files = data.get("Content")

    print("List of files in Server:")
    print(str(files))

#Tell renderer to request the specified file via ID from the Server
def openServerFile():
    print("Getting file")


def closeServerFile():
    print("Closing file")


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
        sys.exit()
    print("\n")
