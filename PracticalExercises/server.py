import socket
import threading

#the HEADER tells us the size of the message we are gonna send
# If the msg is 'Hy' then the server will get a msg of the form
# '5               Hy' where the white space is padding until the msg is 64 bytes
HEADER = 64
PORT = 4444
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "[DISCONNECT]"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

#handle each connection
def handle_client(connection, address):
    #will run concurrent
    print(f"[NEW CONNECTION] {address} connected")

    connected = True
    #When connecting the client sends a blank msg to notify the server
    #An issue will appear when trying to convert it into a int
    while connected:
        #Blocking line of code = we don't pass it until we receive a message
        # Good practice to have them in a thread to ot block the new clients 
        msg_len = connection.recv(HEADER).decode(FORMAT)
        if msg_len:
            msg_len = int(msg_len)
            message = connection.recv(msg_len).decode(FORMAT)
            if message == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{address}] {message}")
    
    connection.close()


#Handle new connection that arrives
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()
        #How many threads are active/ thread active = client
        print(f"[ACTIVE CONNECTION] {threading.active_count() - 1}")

print('[STARTING] server is starting...')
start()