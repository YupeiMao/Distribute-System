import socket
import argparse
import threading

central = "sp19-cs425-g04-01.cs.illinois.edu"

server_checked = False
client_checked = False

# holds all the connection of server
connections = []
def buildServer(port):
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


def connectServer(port, name):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        host = socket.gethostbyname(central)
        sock.connect((host, port))
    except Exception as e:
        print("fail to connect to central")
    send_str = "CONNECT " + name + " " + str(socket.gethostname()) + " " + str(port) + "\n"
    sock.send((send_str.encode()))
    while True:
        data = sock.recv(2048)
        if(handle_reply(data)):
            break
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
def main():
    #parse the command line
    parser = argparse.ArgumentParser(description = "Distributed Chat")
    parser.add_argument('name', type=str)
    parser.add_argument('port',type=int)

    args = parser.parse_args()
    name = args.name
    port = args.port

    server = threading.Thread(target=buildServer, args=(port,))
    client = threading.Thread(target=connectServer, args=(port, name))

    server.start()
    client.start()


if __name__ == '__main__':
    main()
