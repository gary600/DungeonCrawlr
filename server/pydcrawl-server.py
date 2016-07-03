import socket
import socketserver
import json
import time
import sys

def log(str):
	output = "[{}]: {}".format(time.strftime("%H:%M:%S"), str)
	sys.stdout.write(output)
	logfile = open("server.log", "a")
	logfile.write(output)
	logfile.close()

class ConnectError(Exception):
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
			log("New connection from {} with username {}".format(self.client_address[0], self.data["data"]["username"]))
			while True:
				self.dataRaw = self.request.recv
		except ValueError:
			log("Invalid JSON from {}".format(self.client_address[0]))
		except ConnectError:
			log("Invalid request from {}".format(self.client_address[0]))
		