'''
The server will be the external device
Reference Material
https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client#python-socket-example
https://realpython.com/python-sockets/ 
https://www.youtube.com/watch?v=5G_bNVKdECk 
'''
import socket
import select
from threading import Thread

# The server will be running on the same machine as the client for testing purposes, so we can use localhost
# Change later!!
HOST = "127.0.0.1" 
PORT = 5000 

server_socket_list = [] # List of all server sockets objects
listening_socks = [] # List of all listening sockets for select
sending_socks = [] # List of all sending sockets for select

class ServerSocket:
    """Create and manage server sockets"""
    client_list = []

    def __init__(self, host, port):
        """Inititalize a TCP socket """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Get instance
        self.socket.bind((host, port)) # Bind host and port
        self.socket.listen(5) # Enables server to accept connections

    def listen_for_client(self):
        """
        Listen for connections on the main thread
        Route connections to new threads for handling, adding to client list
        """
        # Accept new connection: new socket obj and address bound on client-side
        # Connection architecture officially established
        conn, address = self.socket.accept()
        print("Connection from " + str(address)) # Should be client's

        data = conn.recv(1024).decode() # receive data <=1024 bytes

        # Create new client reference
        client = {'cli_id': data, 'cli_socket': conn}
        print("from connected user " + str(data))

        # Create new thread for client
        ServerSocket.client_list.append(client)
        Thread(target=self.handle_new_client, args=(client,)).start()

    def handle_new_client(self, client):
        """Handle clients when on new thread"""
        cli_id = client['cli_id']
        cli_socket = client['cli_socket']
        while True:
            # Listen for messages
            cli_msg = cli_socket.recv(1024).decode()

            # Print for debugging purposes
            print(str(cli_msg))

    def broadcast_message(self, sender_id, message):
        '''Broadcast a message to all clients (testing purposes)'''
        for cli in self.client_list:
            cli_id = cli['cli_id']
            cli_socket = cli['cli_socket']
            if cli_id != sender_id:
                cli_socket.send(message.encode())

def find_matching_ServerSocket_obj(socket):
    '''Find the ServerSocket object that corresponds to the socket that select is listening to'''
    for server_socket in server_socket_list:
        if server_socket.socket == socket:
            return server_socket

for i in range(3):
    server_socket = ServerSocket(HOST, PORT+i)
    listening_socks.append(server_socket.socket)
    server_socket_list.append(server_socket)
    print("Server socket created on port " + str(PORT+i))

while True:
    try:
        read_socks, write_socks, except_socks = select.select(listening_socks, [], [], 0.5)
        print("read_socks: " + str(read_socks))
    except:
        print("ts broken brochacho")

    for sock in read_socks:
        server_socket = find_matching_ServerSocket_obj(sock)
        server_socket.listen_for_client()

# End-of-file (EOF)
