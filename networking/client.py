'''
The client will be the RPI and its subsystems
Reference Material
https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client#python-socket-example
https://realpython.com/python-sockets/ 
https://www.youtube.com/watch?v=5G_bNVKdECk 
'''
import socket
from threading import Thread
import os

# host is the ip of the server, can be found by running "ipconfig" in terminal and looking for IPv4 address
HOST = "192.168.0.224" 
PORT = 5000

class ClientSocket:
    """Create and manage clients"""
   
    def __init__(self, host, port, id):
        self.client_socket = socket.socket() # Get instance
        # Bind host and port
        # Connection officially established
        print(host + ":" + str(port))
        self.client_socket.connect((host, port))
        self.id = id

        self.talk_to_server()

    def talk_to_server(self):
        '''
        Send over the client name then listen for messages on a seperate thread 
        while sending remains on main
        '''
        self.client_socket.send(self.id.encode()) # send message
        Thread(target = self.receive_message).start()

    def send_message(self, msg):
        '''Send a message to main thread'''
        while True:
            cli_message = self.id + ": " + msg
            self.client_socket.send(cli_message.encode())

    def receive_message(self):
        '''Receive server info from a seperate thread'''
        while True:
            server_message = self.client_socket.recv(1024).decode()
            if not str(server_message).strip():
                os._exit(0)
            print("\n" + server_message)

# Set up all necessary connections to the server
necessary_connections = ["telemetry", "camera", "pilot"]
client_list = [] 

for conn in range(len(necessary_connections)):
    client = ClientSocket(HOST, PORT+conn, necessary_connections[conn])
    client_list.append(client)

# Testing sending a lot of message across threads
while True:
    for client in client_list:
        client.send_message('Hello, server!')

# End-of-file (EOF) 
