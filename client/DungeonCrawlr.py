import socket
import json

with open("config.json") as conffile:
	conf = json.load(conffile)

serverAddr = tuple(conf["server"]["address"])

with socket.socket() as sock:
	sock.connect(serverAddr)
	
