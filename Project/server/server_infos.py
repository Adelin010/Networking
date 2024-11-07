import socket as sock
from socket import socket
import threading as th
from typing import TypeAlias


# Types for a better understading of the code
# Each type starts with a _ 
_Addr: TypeAlias = any
_nickname: TypeAlias = str 
_routing_path: TypeAlias = str

#get the ip addres and the port
SERVER = sock.gethostbyname(sock.gethostname())
PORT = 9898
ADDR = (SERVER, PORT)
#list for the Sockets objects that are connecting
CLIENT_LIST: list[socket] = []
THREADS: list[th.Thread] = []
DATABASE_PATH = "./server/logs.csv"
FORMAT = 'utf-8'
BUF = 1024
#DNS mapping between addr and a nickname
DNS: dict[_Addr, tuple[_nickname, _routing_path]] = {}
#Path of the current page



