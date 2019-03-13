import socket
import argparse
import threading

central = "sp19-cs425-g04-01.cs.illinois.edu"

server_checked = False
client_checked = False

# holds all the connection of server
connections = []

def buildServer(port):
    #create server sock for listening
    sockForListen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockForListen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #initialize socket

    host = socket.gethostname()
    sockForListen.bind((host,port))
    s.listen()
    c, a = sockForListen.accept()

    while True:
        data = c.recv(1024)
        if not data:
            # print fail message
            fail = " has left"
            print(fail)
            c.close()
            break
        print(data)


def connectServer(port, name):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        host = socket.gethostbyname(central)
        sock.connect((host, port))
    except Exception as e:
        print("fail to connect to central")
    send_str = "CONNECT {} {} {}".format(name,socket.gethostname(), port)
    sock.send(bytes(send_str,'utf-8'))

def main():
    #parse the command line
    parser = argparse.ArgumentParser(description = "Distributed Chat")
    parser.add_argument('name', type=str)
    parser.add_argument('port',type=int)

    args = parser.parse_args()
    name = args.name
    port = args.port

    server = threading.Thread(target=buildServer, args=(port))
    client = threading.Thread(target=connectServer, args=(port, name))

    server.start()
    client.start()


if __name__ == '__main__':
    main()
