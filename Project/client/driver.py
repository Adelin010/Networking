import socket as sock
from socket import socket 


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

        while True:
            msg = input("~")
            if(msg == "/quit"):
                send_msg(msg, conn)
                break
            send_msg(msg, conn)
            received_msg = conn.recv(1024).decode()
            if received_msg != '':
                print(received_msg)

    except KeyboardInterrupt:
        conn.close()
        print("User checkedout...")



if __name__ == "__main__":
    main()