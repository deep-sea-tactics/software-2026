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


# Solely for test purposes
# Run tests on same machine
testing: bool = False

HOST = "0.0.0.0"
PORT = 5000

class Client:
    """Create and manage clients"""
   
    def __init__(self, host, port):
        self.client_socket = socket.socket() # Get instance
        # Bind host and port
        # Connection officially established
        self.client_socket.connect((host, port))
        self.id = input("Service ID: ")

        self.talk_to_server()

    def talk_to_server(self):
        '''
        Send over the client name then listen for messages on a seperate thread 
        while sending remains on main
        '''
        self.client_socket.send(self.id.encode()) # send message
        Thread(target = self.receive_message).start()
        self.send_message()

    def send_message(self):
        '''Get user input then send the message to main thread'''
        while True:
            cli_input = input("Your awesome message: ")
            cli_message = self.id + ": " + cli_input
            self.client_socket.send(cli_message.encode())

    def receive_message(self):
        '''Receive server info from a seperate thread'''
        while True:
            server_message = self.client_socket.recv(1024).decode()
            if not str(server_message).strip():
                os._exit(0)
            print("\n" + server_message)

client = Client(HOST, PORT)
# End-of-file (EOF)
