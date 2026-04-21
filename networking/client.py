import socket
from threading import Thread
import os

# The server's static IP address 
# For reference: The RPI's IP address is 192.168.0.2
HOST = "192.168.0.1" 

client_list = [] # List of all clients for later use with broadcasting messages

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
        client_list.append(self)
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


# Testing
if __name__ == "__main__":
    # Set up all necessary connections to the server
    port = 5000

    necessary_connections = ["telemetry", "camera", "controls"]

    for conn in range(len(necessary_connections)):
        client = ClientSocket(HOST, port+conn, necessary_connections[conn])

    # Testing sending a lot of message across threads
    while True:
        for client in client_list:
            print("Sending message from " + client.name)
            client.send_message('Hello, server from port ' + str(port+necessary_connections.index(client.name)))

# End-of-file (EOF) 
