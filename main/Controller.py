###
# Controller class
# Displays the menu to the user
# Tells the Renderer to request a file from the Server
###

import sys

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
    print("List of files in Server:")
    print("1. Blah")
    #Stuff


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