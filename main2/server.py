import os
import os.path as path
import functools
import socket
import json
import protocol_util as util


def request_loop():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Prepare a sever socket
    server_socket.bind((util.SERVER_IP, util.SERVER_PORT))
    server_socket.listen(5)
    print("Server: ready to serve")
    while True:
        # Establish the connection
        connection_socket, _ = server_socket.accept()
        req = util.get_request(connection_socket)
	#print("Content Type: ", req["type"])
        if req is None:
            print("client closed connection, closing ours")
            connection_socket.close()
        elif req["type"] == "list":
            content = list_pwd()
            header = {"contentType": "utf-8"}
            util.send_ok(header, content, connection_socket)
        elif req["type"] == "get":
	    #print("Received request for a file")
            filename = req["filename"]
            result = get_file(filename)
            if result is None:
                util.send_err("No such file named \"{}\"".format(
                    filename), connection_socket)
            else:
                header = {"contentType": "utf-8"}
		#print("connection sock boyo: ", connection_socket)
                util.send_ok(header, result, connection_socket)
        else:
            util.send_err("Unsupported request operation", connection_socket)
        connection_socket.close()
    server_socket.close()


def get_file(filename):
    try:
        file = open(filename, "r")
        # NOTE: we are simply assuming all of our files are valid utf-8.
        # This needs to be altered when reading binary formats like PNG
        s = file.read().decode("utf-8")
        file.close()
        return s
    # normalize exceptions into None
    # since python 2 only has IOError,
    # assume that it's the case where the file was not found
    except IOError:
        return None


def list_pwd():
    # return the list of all files in the present directory. Isn't recursive (doesn't list files in subdirectories)
    mypath = os.getcwd()
    onlyfiles = [f for f in os.listdir(
        mypath) if path.isfile(path.join(mypath, f))]

    return functools.reduce(lambda acc, file: acc + "\n" + file, onlyfiles)


request_loop()
