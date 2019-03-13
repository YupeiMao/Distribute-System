import socket
import threading
import sys
import time
import argparse
from threading import Lock


# hard-coded IP addresses for service
address = "sp19-cs425-g04-01.cs.illinois.edu"

# hard-coded IP addresses for service
port = 4444

# holds all the connection of server
connections = []


# build server for other nodes
def build_server(port):
    # set up sock for listening one node
    sockForListen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockForListen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # create server
    host = socket.gethostname()
    sockForListen.bind((host, port))
    sockForListen.listen(5)

    while True:
        c, a = sockForListen.accept()
        # create thread for this connection listening
        cThread = threading.Thread(target=handle_node, args = (c,a))
        cThread.daemon = True
        cThread.start()
        connections.append(c)


# handler for receiving messages from one node
def handle_node(c, a):
	# receiving messages from this node
	while True:
		data = c.recv(2048)

		# failure detector using EOF
		if not data:
			# print fail message
			c.close()
			break

		handle_transaction(str(data))

# handle one introduce node
def handle_introduce(line):
	neighbor = line.split(" ")




# handle transaction
# IMPORTANT gossip here
def handle_transaction(line):
	transaction = line.split(" ")



def handle_reply(data):
	if (str(data) == "QUIT" or str(data) == "DIE"):
		return 1
	reply = str(data).split("\n")
	for line in reply:
		word = line.split(" ")
		if (word[0] == "INTRODUCE"):
			handle_introduce(line)
		elif (word[0] == "TRANSACTION"):
			handle_transaction(line)
	return 0


# connect to service and handle the response
def connect_service(port, name):
	# create socket for service
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.connect((socket.gethostbyname(address), port))
	host = socket.gethostname()
	# send CONNECT to service
	msg = "CONNECT " + name + " " + str(host) + " " + str(port) + "\n"
	sock.send(msg.encode())
	# start receiving message from service
	while True:
		data = sock.recv(2048)
		if(handle_reply(data)):
			break


def main():
	# parse the command line
	parser = argparse.ArgumentParser(description = 'Cryptocurrency')
	parser.add_argument('name', type=str)
	parser.add_argument('port', type=int)
	args = parser.parse_args()
	name = args.name
	port = args.port

	server = threading.Thread(target=build_server, args=(port, ))
	# client = threading.Thread(target=connectService, args=(port, ), kwargs={"name": name})
	client = threading.Thread(target=connect_service, args=(port, name))

	# start server and client
	server.start()
	client.start()

# entry point for application
if __name__ == '__main__':
    main()
