# Program that detects open server on lan in real time
# Made by 0ev

import socket
import struct
import time
import threading
from kaling import Kakao
from datetime import datetime
import json

# Get my personal information
with open('info.json') as json_file:
    data = json.load(json_file)


global ROOM
ROOM = "예상우"


KakaoLink = Kakao(data["jskey"],'http://students.ksa.hs.kr')
KakaoLink.login(data["mail"],data["pwd"])

current_server = {}

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

def check_server():
    global current_server
    while True:
        delete = []
        for x in current_server:
            if current_server[x][1] < time.time() - 5:
                threading.Thread(target=server_end, args=(x,current_server[x])).start()
                delete.append(x)
        for x in delete:
            current_server.pop(x)
        time.sleep(1)

def server_end(ad,server):
    print(f"server {server[0]} on {ad} has been shut down")
    KakaoLink.send(ROOM,{
            "link_ver": "4.0",
            "template_object": {
                "object_type": "feed",
                "button_title": "",
                
                "content": {
                    "title": f"서버 {server[0]} 가 {ad}에서 닫혔습니다",
                    "image_url": "",
                    "image_height" : 150,
                    "image_width" : 600,
                    "link": {
                        "web_url": "",
                        "mobile_web_url": ""
                    },
                    "description": f"closed at : {server[1]}"
                },
            }
        })



def server_start(ad,server):
    print(f"server {server[0]} has been opened on {ad}")
    KakaoLink.send(ROOM,{
            "link_ver": "4.0",
            "template_object": {
                "object_type": "feed",
                "button_title": "",
                
                "content": {
                    "title": f"서버 {server[0]} 가 {ad}에서 열렸습니다!",
                    "image_url": "",
                    "image_height" : 150,
                    "image_width" : 600,
                    "link": {
                        "web_url": "",
                        "mobile_web_url": ""
                    },
                    "description": f"opened at : {server[1]}"
                },
            }
        })

def tag_server():
    global current_server
    while True:
        data, address = sock.recvfrom(1024)
        data = data.decode("utf-8")
        name = find('MOTD',data)
        address = f"{address[0]}:{find('AD',data)}"

        if address in current_server:
            current_server[address][1] = time.time()

        else:
            current_server[address] = [name, time.time()]
            threading.Thread(target=server_start, args=(address,[name,time.time()])).start()

print("Starting...")
check_thread = threading.Thread(target=check_server)
tag_thread = threading.Thread(target=tag_server)
check_thread.start()
tag_thread.start()
