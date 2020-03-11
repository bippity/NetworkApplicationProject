import socket
import sys
import json
import protocol_util as util


def perform_request(args):
	#print(args)
	num_args = len(args)
	if num_args < 1 or num_args > 2:
		print("invalid command\n usage: list | render <filename> | play | pause | restart")
		return


	if num_args == 1 and args[0] == "list":
		# Connect to server and get list of files
		request = util.create_list_request()
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((util.SERVER_IP, util.SERVER_PORT))
		util.send_request(request, sock)
		header, content = util.get_response(sock)
		# Print out response
		if header["status"] == "OK":
			print("\nAvailable Files:\n")
			print(content)
			
		elif header["status"] == "ERROR":
			# log("got an error from the server")
			print(header["errorMessage"])
		else:
			print("unknown status type")

		sock.close()
	
	elif num_args == 1 and args[0] == ("help"):
		help()

	elif num_args == 2 and args[0] == "render":
		file = args[1]
		request = util.create_render_request(file)
		renderer_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		renderer_sock.connect((util.RENDERER_IP, util.RENDERER_PORT))
		util.send_request(request, renderer_sock)

		header, content = util.get_response(renderer_sock)
		# Print out response
		if header["status"] == "OK":
			print(content)
		elif header["status"] == "ERROR":
			# log("got an error from the server")
			print(header["errorMessage"])
		else:
			print("unknown status type")
		print("Closing render socket")
		renderer_sock.close()

	elif num_args == 1 and args[0] == "play":
		request = util.create_play_request()
		renderer_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		renderer_sock.connect((util.RENDERER_IP, util.RENDERER_PORT))
		util.send_request(request, renderer_sock)

		header, content = util.get_response(renderer_sock)
		# Print out response
		if header["status"] == "OK":
			print(content)
		elif header["status"] == "ERROR":
			# log("got an error from the server")
			print(header["errorMessage"])
		else:
			print("unknown status type")

		renderer_sock.close()

	elif num_args == 1 and args[0] == "pause":
		request = util.create_pause_request()
		renderer_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		renderer_sock.connect((util.RENDERER_IP, util.RENDERER_PORT))
		util.send_request(request, renderer_sock)

		header, content = util.get_response(renderer_sock)
		# Print out response
		if header["status"] == "OK":
			print(content)
		elif header["status"] == "ERROR":
			# log("got an error from the server")
			print(header["errorMessage"])
		else:
			print("unknown status type")

		renderer_sock.close()

	elif num_args == 1 and args[0] == "restart":
		request = util.create_restart_request()
		renderer_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		renderer_sock.connect((util.RENDERER_IP, util.RENDERER_PORT))
		util.send_request(request, renderer_sock)

		header, content = util.get_response(renderer_sock)
		# Print out response
		if header["status"] == "OK":
			print(content)
		elif header["status"] == "ERROR":
			# log("got an error from the server")
			print(header["errorMessage"])
		else:
			print("unknown status type")

		renderer_sock.close()
	else:
		print("ERROR: Invalid command\n usage: list | render <filename> | play | pause | restart | help")
		return

def help():
	print("\n\nHello! Using our protocol is very simple. Make\nsure to access controller (the screen you're\nlooking at) when using any commands. To get a\nlist of your available files, simply type \"list\".\nTo get a file, simply type:\n\n--------------------------------------\nrender exampleFile.txt\n--------------------------------------\n\nThe same goes for play, pause, and restart:\n--------------------------------------\nplay/pause/restart exampleFile.extension\n--------------------------------------\n")
	raw_input("Press any key to continue...\n")

while True:
	args = raw_input("\nEnter your command from the following:\nlist\nrender <filename>\nplay\npause\nrestart\nhelp\n\nCommand: ")
	perform_request(args.split(' '))
