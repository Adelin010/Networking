import socket as sock
import threading as th

HEADER = 64
PORT = 6457
SERVER = '127.0.1.1'
DICONNECT_MSG = '#DIS'

ADDR = (SERVER, PORT)
FORMAT = 'utf-8'


client = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
client.connect(ADDR)

def msg_check():
    while True:
        try:
            message = client.recv(2048).decode(FORMAT)
            print(message)
        except KeyboardInterrupt:
            break 


def send_msg(msg):
    #find the length of the message that the server will send
    message = msg.encode(FORMAT)
    msg_len = len(message)
    #get the length of the message make an encode 
    #then add white spaces until we reach the size
    send_length = str(msg_len).encode(FORMAT)
    send_length += b' '*(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

def client_main():
    connected = True 
    send_msg("Connection Established...")
    while connected:
        try: 
            message = input("Message?: ")
            if message == 'disconnect':
                connected = False
                break
            send_msg(message)
        except KeyboardInterrupt: 
            connected = False
            break 
    send_msg(DICONNECT_MSG)


client_main()