# Program that detects open server on lan
# Made by 0ev

import socket
import struct
import asyncio

multicast_group = '224.0.2.60'
server_address = ('', 4445)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(server_address)
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

async def check_server():
    while True:
        print(1)
        await asyncio.sleep(1)
            

async def tag_server():
    while True:
        data, address = sock.recvfrom(1024)
        data = data.decode("utf-8")
        print(data, address)

# Create tasks
async def main():
    await asyncio.gather(check_server(),tag_server())

# Run
asyncio.run(main())