import socket
'''
The client will be the external device (laptop)
'''

# Solely for test purposes
# Run tests on same machine
testing: bool = True;

if (not testing):
    HOST = "192.168.0.225"  #225 is an arbitrary number
else:
    # Returns current machine hostname
    HOST = socket.gethostname() 
PORT = 5000

clientSocket = socket.socket() # Get instance
clientSocket.connect((HOST, PORT)) # Bind host and port

# Server-Client architecture officially established

message = input(">")

while message.lower().strip() != 'bye':
    clientSocket.send(message.encode()) # send message
    data = clientSocket.recv(1024) # receive response

    print("Received from server: " + str(data))

    message = input(">")

clientSocket.close()