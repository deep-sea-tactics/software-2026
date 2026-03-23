import socket
'''
The server will be the RPI
Reference Material
https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client#python-socket-example
https://realpython.com/python-sockets/ 
'''

# Solely for test purposes
# Run tests on same machine
testing: bool = True;

if (not testing):
    # Double check if this is the right IP address
    HOST = "192.168.0.1" 
else:
    # Returns current machine hostname
    HOST = socket.gethostname() 
PORT = 5000

servSocket = socket.socket() # Get instance
servSocket.bind((HOST, PORT)) # Bind host and port
servSocket.listen() # Enables server to accept connections

# accept new connection: new socket obj and address bound on client-side
conn, address = servSocket.accept() 

# Server-Client architecture officially established

print("Connection from " + str(address)) # Should be client's
while True:
    data = conn.recv(1024) # receive data <=1024 bytes
    if not data: # Checks if data is received
        break
    print("from connected user " + str(data))
    data = input('>')
    conn.send(data.encode()) # Send data to client
    