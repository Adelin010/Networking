import socket as sock
from socket import socket
import threading as th

# We must create 2 Threads to handle the client correcly
# Thread1 = handles writting the messages 
# Thread2 = handles the reading from server
# !! This way we can write independet from the receiving 

#get the ip addres and the port
SERVER = "127.0.1.1"
PORT = 9898
ADDR = (SERVER, PORT) 
FORMAT = 'utf-8'

def send_msg(msg: str, connection: socket):
    connection.sendall(msg.encode(FORMAT))


def singin(connection: socket) -> None:
    #get the Username
    username = input(connection.recv(1024).decode())
    send_msg(username, connection)
    #get the Password
    password = input(connection.recv(1024).decode())
    send_msg(password, connection)


def login(connection:socket) -> None:
     #get the login page
    username = input(connection.recv(1024).decode())
    send_msg(username, connection)
    password = input(connection.recv(1024).decode())
    send_msg(password, connection)


def chating_send(connection: socket) -> None:
    while True:
        msg = input("~")
        if(msg == "/quit"):
            send_msg(msg, connection)
            break
        send_msg(msg, connection)


def chating_receive(connection: socket) -> None:
    while True:
        msg = connection.recv(1024).decode()
        if msg != '':
            print(msg)


def main():
    conn = socket(sock.AF_INET, sock.SOCK_STREAM)
    
    try:
        conn.connect(ADDR)
        logged = input(conn.recv(1024).decode())
        conn.sendall(logged.encode(FORMAT))
        if logged == "/singin":
            print(conn.recv(1024).decode())
            singin(conn)
        print(conn.recv(1024).decode())
        login(conn)
        #display checking username message
        print(conn.recv(1024).decode())
        print("Chat\n")

        th_seding = th.Thread(target=chating_send, args=(conn))
        th_receive = th.Thread(target=chating_receive, agrs=(conn))
        th_receive.start()
        th_seding.start()
    except KeyboardInterrupt:
        conn.close()
        print("User checkedout...")



if __name__ == "__main__":
    main()