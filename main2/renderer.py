# general idea
# establish a "permenant" connection to the controller
#   - when we receive a message from the controller, establish a temporary connection with the server
#   - forward that request to the server
#   - when we get the message from the server, render it the contents of the message
import socket
import protocol_util as util


def render_loop():
	# setup port for controller to connect to
	renderer_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	renderer_sock.bind((util.RENDERER_IP, util.RENDERER_PORT))
	renderer_sock.listen(5)

	log("able to render")
	while True:

		connection_sock, _ = renderer_sock.accept()
		req = util.get_request(connection_sock)
		print("Request!! ", req)

		if req is None:
			log("controller closed their end, closing ours")
			connection_sock.close()
		elif req["type"] == "render":
			global content
			content = req["filename"]
			# establish a temporary connection to the server.
			server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server_sock.connect((util.SERVER_IP, util.SERVER_PORT))
			request = util.create_get_request(content)
			util.send_request(request, server_sock)

			header, cont = util.get_response(server_sock)
			if header is None and content is None:
				# log("weird header")
				util.send_err("malformed header", connection_sock)
			elif header["status"] == "OK":
				# log("we are ok")
				util.send_empt_ok(header, connection_sock)
				render(cont)
			elif header["status"] == "ERROR":
				# log("got an error from the server")
				util.send_err(header["errorMessage"], connection_sock)
				log(header["errorMessage"])
			else:
				# log("unknown status type")
				util.send_err("unknown status type", connection_sock)

			# cleanup temporary socket
			server_sock.close()

		elif req["type"] == "play":
			if content is not None:
				# establish a temporary connection to the server.
				server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				server_sock.connect((util.SERVER_IP, util.SERVER_PORT))
				request = util.create_get_request(content)
				util.send_request(request, server_sock)

				header, cont = util.get_response(server_sock)
				if header is None and content is None:
					# log("weird header")
					util.send_err("malformed header", connection_sock)
				elif header["status"] == "OK":
					# log("we are ok")
					util.send_empt_ok(header, connection_sock)
					render(cont)
				elif header["status"] == "ERROR":
					# log("got an error from the server")
					util.send_err(header["errorMessage"], connection_sock)
					log(header["errorMessage"])
				else:
					# log("unknown status type")
					util.send_err("unknown status type", connection_sock)

				# cleanup temporary socket
				server_sock.close()
			else:
				util.send_err("No file loaded, please use render command first.", connection_sock)
		elif req["type"] == "pause":
			if content is not None:
				send_empty_ok(connection_sock)
			else:
				util.send_err("No file loaded, please use render command first.", connection_sock)
		elif req["type"] == "restart":
			if content is not None:
				# establish a temporary connection to the server.
				server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				server_sock.connect((util.SERVER_IP, util.SERVER_PORT))
				request = util.create_get_request(content)
				util.send_request(request, server_sock)

				header, cont = util.get_response(server_sock)
				if header is None and content is None:
					# log("weird header")
					util.send_err("malformed header", connection_sock)
				elif header["status"] == "OK":
					# log("we are ok")
					util.send_empt_ok(header, connection_sock)
					render(cont)
				elif header["status"] == "ERROR":
					# log("got an error from the server")
					util.send_err(header["errorMessage"], connection_sock)
					log(header["errorMessage"])
				else:
					# log("unknown status type")
					util.send_err("unknown status type", connection_sock)

				# cleanup temporary socket
				server_sock.close()
			else:
				util.send_err("No file loaded, please use render command first.", connection_sock)
			
		# cleanup after transaction occurs
		connection_sock.close()

	# cleanup
	renderer_sock.close()


def send_empty_ok(socket):
	util.send_ok(dict(), "", socket)


def init():
	global content
	global content_type
	content = None
	content_type = None


def load_content(new_content):
	global content
	content = new_content


def render(content):
	print(">")
	print(content)
	print("<")


def log(msg):
	print("Renderer: {}".format(msg))


init()
render_loop()
