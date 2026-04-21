
''' ignore for the moment
import paramiko
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# start server

# start client to RPI using SSH
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect(hostname='192.168.0.2', username=os.getenv('rpi_username'), password=os.getenv('rpi_password'))
(stdin, stdout, stderr) = client.exec_command('python3 software-2026/networking/client.py')
stdin.close()
''' 

