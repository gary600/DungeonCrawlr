import socket
import socketserver
import json
import time
import sys

class serverInfo:
	VERSION = 0.1

class loglevels:
	INFO = "INFO"
	WARN = "WARN"
	FATAL = "FATAL"

def log(str, loglevel):
	output = "[{}] [{}]: {}".format(time.strftime("%H:%M:%S"), loglevel, str)
	sys.stdout.write(output)
	with open("server.log", "a") as logfile:
		logfile.write(output)

class ConnectError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
		
class OutdatedClientError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class OutdatedServerError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class ConnectionHandler(socketserver.BaseRequestHandler):
	def handle(self):
		self.dataRaw = self.request.recv(1024).strip()
		try:
			self.data = json.loads(self.dataRaw.decode())
			if self.data["connectType"] != "request_connect":
				raise ConnectError
			if self.data["data"]["clientVersion"] != serverInfo.version:
				raise OutdatedClientError
			log("Incoming connection from {} with username {}".format(self.client_address[0], self.data["data"]["username"]), loglevels.INFO)
			while True:
				self.dataStreamRaw = self.request.recv(1024).strip()
				self.dataStream = json.loads(self.dataStreamRaw.decode())
				self.connectType = self.dataStream["connectType"]
				if self.connectType[0] == "request":
					if self.connectType[1] == "disconnect":
						break
					elif self.connectType[1] == "chat":
						pass
				elif self.connectType[0] == "put":
					if self.connectType[1] == "movement":
						pass
					elif self.connectType[1] == "chat":
						pass
		except ValueError:
			log("{} lost connection: Invalid JSON".format(self.client_address[0]), loglevels.INFO)
		except ConnectError:
			log("{} lost connection: Invalid request".format(self.client_address[0]), loglevels.WARN)
		except OutdatedClientError:
			log("{} lost connection: Outdated client (client version {f})".format(self.client_address[0],self.data["data"]["clientVersion"]), loglevels.INFO)
		except OutdatedServerError:
			log("{} lost connection: Outdated server (client version {f})".format(self.client_address[0],self.data["data"]["clientVersion"]), loglevels.INFO)