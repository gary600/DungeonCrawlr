import socket
import socketserver
import json
import time
import sys

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

class ConnectionHandler(socketserver.BaseRequestHandler):
	def handle(self):
		self.dataRaw = self.request.recv(1024).strip()
		try:
			self.data = json.loads(self.dataRaw.decode())
			if self.data["connectType"] != "request_connect":
				raise ConnectError
			if self.data["data"]["clientVersion"]
			log("New connection from {} with username {}".format(self.client_address[0], self.data["data"]["username"]), loglevels.INFO)
			while True:
				self.dataRaw = self.request.recv(1024).strip()
		except ValueError:
			log("Invalid JSON from {}".format(self.client_address[0]), loglevels.INFO)
		except ConnectError:
			log("Invalid request from {}".format(self.client_address[0]), loglevels.WARN)
		except OutdatedClientError:
			log("Outdated client from {}".format(self.client_address[0]), loglevels.INFO)