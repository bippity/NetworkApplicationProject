# protocol utils. Shared info that all parts need to have
# general philosophy is to fail fast. Ensure invariants are upheld and if they aren't,
# throw an exception ASAP. This makes debugging far quicker and we don't let weird behavior through
import json

NUM_LEN = 4
MAX_HEADER_LEN = (10 ** (NUM_LEN + 1)) - 1
SERVER_PORT = 3029
RENDERER_PORT = 3042
SERVER_IP = '10.0.0.1'
RENDERER_IP = '10.0.0.2'
CONTROLLER_IP = '10.0.0.3'


def pad_num(num):
	len_str = str(num)
	padding_amount = NUM_LEN - len(len_str)
	pad = ""
	for _ in range(0, padding_amount):
		pad += " "
	return pad + len_str



# Creating jsons for requests
def create_list_request():
	request = {"type": "list"}
	return request


def create_render_request(file_name):
	request = {"type": "render", "filename": file_name}
	return request


def create_get_request(file_name):
	request = {"type": "get", "filename": file_name}
	return request


def create_play_request():
	request = {"type": "play"}
	return request


def create_pause_request():
	request = {"type": "pause"}
	return request


def create_restart_request():
	request = {"type": "restart"}
	return request


# sending and getting requests


def request_to_string(request):
	req_type = request.get("type")
	"""
	req_type = request.get("type")
	if req_type is None:
		raise InvalidRequest("need a type of request to send")
	elif req_type != "list" and req_type != "play" and req_type != "pause" and req_type != "restart":
		if req_type == "get" or req_type == "render":
			if not request.has_key("filename"):
				raise InvalidRequest(
					"With a get request, need a file to request")
		else:
			raise InvalidRequest("Unknown request type")
	"""
	return "{}{}".format(
		request["type"], "" if (req_type == "list" or req_type == "play" or req_type == "pause" or req_type == "restart") else (" " + request["filename"]))


def send_request(request, socket):
	req_str = request_to_string(request)
	send_raw_request(req_str, socket)


def send_raw_request(request_str, socket):
	req_len = pad_num(len(request_str))
	socket.sendall(req_len)
	socket.sendall(request_str)


def get_raw_request(socket):
	raw = socket.recv(NUM_LEN).decode("ascii")
	# empty messages are a signal from the transmitter that they are closing the connection
	if raw == "":
		return None
	length = int(raw)
	request = socket.recv(length).decode("ascii")
	# print(request)
	return request


def get_request(socket):
	raw_req = get_raw_request(socket)
	return string_to_request(raw_req)


def string_to_request(req_str):
	if req_str is None:
		return None
	elif req_str == "list":
		return {"type": "list"}

	req = req_str.split(" ")
	req_len = len(req)

	if req_len == 1:
		if req[0] == "list" or req[0] == "play" or req[0] == "pause" or req[0] == "restart":
			return {"type": req[0]}
		else:
			raise InvalidRequest("Unknown request type of " + req[0])
	elif req_len == 2:
		if req[0] == "render" or req[0] == "get":
			return {"type": req[0], "filename": req[1]}
		else:
			raise InvalidRequest("Unknown request type of {} with second value of {}".format(req[0], req[1]))
	else:
		raise InvalidRequest("Unknown request format:\n" + req_str)

# sending and receiving responses (and their headers)

def send_content(content, socket):
	header = {"type": "file"}
	header["contentType"] = "utf-8"
	header["contentLength"] = len(content)
	send_header(header, socket)
	socket.sendall(content)


def send_ok(header, content, socket):
	# header: dictionary of header values. Probably only need to send the encoding type
	# content: string of whatever kind for the receiver to decode
	# socket: the receiver's socket
	header["status"] = "OK"
	header["contentLength"] = len(content)
	send_header(header, socket)
	# send content seperately
	socket.sendall(content)

def send_empt_ok(header, socket):
	header["status"] = "OK"
	header["contentLength"] = 0
	send_header(header, socket)


def send_err(error_msg, socket):
	header = {"status": "ERROR", "errorMessage": error_msg}
	send_header(header, socket)


def send_header(header, socket):
	json_header = json.dumps(header)
	json_len = len(json_header)
	if json_len > MAX_HEADER_LEN:
		raise HeaderTooLong(
			"Header cannot be sent with length {}".format(json_len))

	header_len = pad_num(json_len)
	socket.send(header_len)
	socket.send(json_header)

# obtains the response from the transmitter as a tuple of the header and the response


def get_response(socket):
	raw_header_len = socket.recv(NUM_LEN).decode("ascii")
	# need to handle the case that the transmitter disconnected
	if raw_header_len == "":
		return None, None

	header_len = int(raw_header_len)
	header = socket.recv(header_len).decode("ascii")
	try:
		header = json.loads(header)
	except ValueError:
		raise InvalidResponse("Response could not be parsed as a JSON")

	if header["status"] == "OK":
		if not header.has_key("contentLength"):
			raise InvalidResponse(
				"Must have content length, even when sending empty messages")

		content_len = int(header["contentLength"])
		# renderer can return an OK with no body, indicated by contentLength = 0
		if content_len == 0:
			return header, None
		elif not header.has_key("contentType"):
			raise InvalidResponse(
				"Must specify the type of content being sent")
		# obtain the actual content of the message
		content = socket.recv(content_len).decode(header["contentType"])
		return header, content
	elif header["status"] == "ERROR":
		if not header.has_key("errorMessage"):
			raise InvalidResponse(
				"Need an error message accompanying what went wrong")
		return header, None
	else:
		raise InvalidResponse("received an unexpected header")


class InvalidResponse(ValueError):
	def __init__(self, arg):
		self.strerror = arg
		self.args = {arg}


class InvalidRequest(ValueError):
	def __init__(self, arg):
		self.strerror = arg
		self.args = {arg}


class HeaderTooLong(ValueError):
	def __init__(self, arg):
		self.strerror = arg
		self.args = {arg}
