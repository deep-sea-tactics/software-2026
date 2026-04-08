'''
The server will be the external device
Reference Material
https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client#python-socket-example
https://realpython.com/python-sockets/ 
https://www.youtube.com/watch?v=5G_bNVKdECk 
'''
import socket
from threading import Thread

# Solely for test purposes
# Run tests on same machine
testing: bool = False

HOST = "127.0.0.1" # local host
PORT = 5000

class Server:
    """Create and manage server"""
    clients_list = []

    def __init__(self, host, port):
        """Inititalize a TCP socket """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Get instance
        self.server_socket.bind((host, port)) # Bind host and port
        self.server_socket.listen(5) # Enables server to accept connections
        print('Server awating connection')

    def listen(self):
        """
        Listen for connections on the main thread
        Route connections to new threads for handling, adding to client list
        """
        while True:
            # Accept new connection: new socket obj and address bound on client-side
            # Connection architecture officially established
            conn, address = self.server_socket.accept()
            print("Connection from " + str(address)) # Should be client's

            data = conn.recv(1024).decode() # receive data <=1024 bytes
            if not data: # Checks if data is received
                break

            # Create new client reference
            client = {'cli_id': data, 'cli_socket': conn}
            print("from connected user " + str(data))

            # Create new thread for client
            Server.clients_list.append(client)
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

            # if message is bye remove clinet
            if cli_msg.lower().strip() == str(cli_id) + ": bye":
                Server.clients_list.remove(client)
                cli_socket.close()
                break
            else:
                # Send message to all other clients
                self.broadcast_message(cli_id, cli_msg)

    def broadcast_message(self, sender_id, message):
        '''Broadcast a message to all clients (testing purposes)'''
        for cli in self.clients_list:
            cli_id = cli['cli_id']
            cli_socket = cli['cli_socket']
            if cli_id != sender_id:
                cli_socket.send(message.encode())

test_server = Server(HOST, PORT)
test_server.listen()
# End-of-file (EOF)
