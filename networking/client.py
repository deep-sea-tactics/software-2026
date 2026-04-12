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

# The server will be running on the same machine as the client for testing purposes, so we can use localhost
# Change later!!
HOST = "127.0.0.1" 
PORT = 5000

class ClientSocket:
    """Create and manage clients"""
   
    def __init__(self, host, port, name):
        self.client_socket = socket.socket() # Get instance
        # Bind host and port
        # Connection officially established
        print(host + ":" + str(port))
        
        try:
            self.client_socket.connect((host, port))
        except:
            print("Failed to connect to server. Is the server running?")
            os._exit(0)
        
        self.name = name
        self.talk_to_server()

    def talk_to_server(self):
        '''
        Send over the client name then listen for messages on a seperate thread 
        while sending remains on main
        '''
        self.client_socket.send(self.name.encode()) # send message
        Thread(target = self.receive_message).start()

    def send_message(self, msg):
        '''Send a message to main thread'''
        cli_message = self.name + ": " + msg
        self.client_socket.send(cli_message.encode())

    def receive_message(self):
        '''Receive server info from a seperate thread'''
        while True:
            server_message = self.client_socket.recv(1024).decode()
            if not str(server_message).strip():
                os._exit(0)
            print("\n" + server_message)

# Set up all necessary connections to the server
necessary_connections = ["telemetry", "camera", "controls"]
client_list = [] 

for conn in range(len(necessary_connections)):
    client = ClientSocket(HOST, PORT+conn, necessary_connections[conn])
    client_list.append(client)

# Testing sending a lot of message across threads
while True:
    for client in client_list:
        print("Sending message from " + client.name)
        client.send_message('Hello, server from port ' + str(PORT+necessary_connections.index(client.name)))

# End-of-file (EOF) 
