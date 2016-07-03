import socket
import socketserver
import json
import time

class ConnectionHandler(socketserver.BaseRequestHandler):
	def handle(self):
		self.dataRaw = self.request.recv(1024).strip()
		try:
			self.data = json.loads(self.dataRaw.decode())
			print("[{}]: Connection from {} with username {}".format(time.strftime("%H:%M:%S"), self.client_address[0], self.data["user"]["name"]))
		except ValueError:
			print("[{}]: Invalid JSON from {}".format(time.strftime("%H:%M:%S"), self.client_address[0]))
		