import socket

HEADER = 64
PORT = 4444
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "[DISCONNECT]"
SERVER = "127.0.1.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg: str):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    #This is the length encoded 
    send_length = str(msg_len).encode(FORMAT)
    #Now we need to padd the length until the 64 bytes 
    #but we do not know the length of this message 
    #thus we subtact it form 64 to know how much to padd
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

send("Gracias !!")
send("I think I will stop")
send(DISCONNECT_MESSAGE)
