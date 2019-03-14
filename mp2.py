import socket
import threading
import sys
import time
import argparse
from threading import Lock


#######################logging#################
import logging
logging.basicConfig(filename='test.log', level=logging.DEBUG)




# hard-coded IP addresses for service
service_address = "sp19-cs425-g04-01.cs.illinois.edu"

# holds all the connection of server
connections = []

# hold all the socket to send message
sockForSend = {}

# count the number of nodes connected
count = 0

# new node to connect in client
newNode = []

# determine if node is infected
infected = False

# lock for new node
add_lock = Lock()

# lock for add lock
conn_lock = Lock()

# lock for node
node_lock = Lock()

# CONNECT msg for connecting nodes, service, and querying for new nodes
msg = ""



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
        cThread = threading.Thread(target=handle_connection, args = (c,a))
        cThread.daemon = True
        cThread.start()
        connections.append(c)


# handler for receiving messages from one node
def handle_connection(c, a):
	# receiving messages from this node
	while True:
		data = c.recv(2048)

		# failure detector using EOF
		if not data:
			# print fail message
			c.close()
			break

		handle_node_msg(data)


# send list of nodes to the new node
def send_list(msg):
	node_lock.acquire()
	for sock in sockForSend:
		sockForSend[sock].send(sock)
	node_lock.release()


# parse and handle the message from other nodes
def handle_node_msg(data):
	temp = data.decode()
	msg = data.decode().split(" ")
	if (msg[0] == "CONNECT"):
		if (temp not in sockForSend):
			add_lock.acquire()
			newNode.append(temp)
			add_lock.release()
		send_list(msg)
	elif (msg[0] == "TRANSACTION"):
		return


# handle one introduce node
def handle_introduce(line):
	neighbor = line.split(" ")
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.connect(line[2], line[3])
	host = socket.gethostname()
	# send CONNECT to the node
	sock.send(msg.encode())

	# add periodally query here
	threading.Timer(1, handle_introduce, args={line,}).start()


def gossip(line):
	target = line.split(" ")


# handle transaction
# IMPORTANT gossip here
def handle_transaction(line):
	transaction = line.split(" ")
	threading.Timer(1, gossip, args=(line,)).start()


# handle message from the service
def handle_service_msg(data):
	if (str(data) == "QUIT" or str(data) == "DIE"):
		return 1
	reply = str(data).split("\n")
	for line in reply:
		logging.debug(line)
		word = line.split(" ")
		if (word[0] == "INTRODUCE"):
			discovery = threading.Thread(target=handle_introduce, args=(line, ))
			discovery.start()
		elif (word[0] == "TRANSACTION"):
			transaction = threading.Thread(target=handle_transaction, args=(line, ))
			transaction.start()

	return 0

# connect to service and handle the response
def connect_service(port, name):
	# create socket for service
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.connect((socket.gethostbyname(service_address), 6666))

	# send CONNECT to service
	sock.send(msg.encode())
	# start receiving message from service
	while True:
		data = sock.recv(2048)
		if(handle_service_msg(data)):
			break


# connect to the nodes that is discovered
def connect_nodes():
	# loop until node is dead
	while True:
		node_lock.acquire()
		if (len(newNode) == 0):
			continue
		# pop the last item to add
		toAdd = newNode.pop(-1)
		node_lock.release()
		# connect to this server
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.connect(toAdd[2], toAdd[3])
		# save the socket
		conn_lock.acquire()
		sockForSend[toAdd] = sock
		conn_lock.release()



def main():
	# parse the command line
	parser = argparse.ArgumentParser(description = 'Cryptocurrency')
	parser.add_argument('name', type=str)
	parser.add_argument('port', type=int)
	args = parser.parse_args()
	name = args.name
	port = args.port

	host = socket.gethostname()
	global msg
	msg = "CONNECT " + name + " " + str(host) + " " + str(port) + "\n"

	server = threading.Thread(target=build_server, args=(port, ))
	# client = threading.Thread(target=connectService, args=(port, ), kwargs={"name": name})
	client_for_service = threading.Thread(target=connect_service, args=(port, name))
	client_for_nodes = threading.Thread(target=connect_nodes)

	# start server and client
	server.start()
	client_for_service.start()
	client_for_nodes.start()

# entry point for application
if __name__ == '__main__':
    main()
