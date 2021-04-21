# Program that creates a fake minecraft server on lan
# Can be used to reroute players to actual server
# Made by 0ev

import socket
import asyncio

# Create server with motd and port
async def create_server(motd,ad):
    MESSAGE = f"[MOTD]{motd}[/MOTD][AD]{ad}[/AD]"
    UDP_IP = "224.0.2.60"
    UDP_PORT = 4445

    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
        print(motd)
        await asyncio.sleep(1.5)

# Create tasks
async def main():
    task1 = asyncio.create_task(create_server("test1",1))
    task2 = asyncio.create_task(create_server("test2",2))
    await task1
    await task2

# Run
asyncio.run(main())