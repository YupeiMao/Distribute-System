import socket
import argparse
import threading

central = "sp19-cs425-g04-01.cs.illinois.edu"

server_checked = False
client_checked = False

# holds all the connection of server
connections = []

def buildServer(port):
    pass









def connectServer(port, name):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        host = socket.gethostbyname(central)
        sock.connect((host, 6666))
    except Exception as e:
        print("Fail to connect to central")
    send_str = "CONNECT " + name + " " + str(socket.gethostname()) + " "+str(port) + "\n"
    # print(send_str)
    sock.send(send_str.encode())

    #receive indroduction
    while True:
        data = sock.recv(2048)
        if(handle_reply(data)):
            break


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

def handle_introduce(line):
	neighbor = line.split(" ")

# handle transaction
# IMPORTANT gossip here
def handle_transaction(line):
	transaction = line.split(" ")


if __name__ == '__main__':
    main()
