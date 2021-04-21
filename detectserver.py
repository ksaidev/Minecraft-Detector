# Program that detects open server on lan
# Made by 0ev

import socket
import struct

multicast_group = '224.0.2.60'
server_address = ('', 4445)

# Create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to server address
sock.bind(server_address)

group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

def find(a,string):
    string = string.split(f"[{a}]")[1]
    string = string.split(f"[/{a}]")[0]
    return string

while True:

    print("\nlistening")
    data, address = sock.recvfrom(1024)

    data = data.decode("utf-8")

    print(f"name : {find('MOTD',data)}")
    print(f"server address : {address[0]}:{find('AD',data)}")
