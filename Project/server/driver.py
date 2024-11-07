import socket as sock
from socket import socket 
import threading as th
from time import sleep

#get the ip addres and the port
SERVER = sock.gethostbyname(sock.gethostname())
PORT = 9898
ADDR = (SERVER, PORT)
#list for the Sockets objects that are connecting
CLIENT_LIST: list[socket] = []
THREADS: list[th.Thread] = []
DATABASE_PATH = "./server/logs.csv"
FORMAT = 'utf-8'
DNS: dict[any, str] = {}

def checkfile(string: str) -> bool:
    with open(DATABASE_PATH, 'r') as db:
        for line in db.readlines():
            if string in line:
                return True
    return False


#function for the start connection
def manageStart(connection:socket, addr) -> str:   
    sleep(1)
    connection.sendall("Enter your username: ".encode(FORMAT))
    #get back the username
    username = connection.recv(1024).decode()
    #send the password massage
    connection.sendall("Enter your password: ".encode(FORMAT))
    #get the password 
    password = connection.recv(1024).decode()
    #write in the database

    if not checkfile(username + ',' + password):
        with open(DATABASE_PATH, 'a') as db:
            db.write(username + ',' + password + '\n')
    DNS[addr] = username
    print(f"DNS: {DNS[addr]}")
    return "/login/"


def manageSignIn(connection: socket, addr) -> str:
    sleep(1)
    connection.sendall("username: ".encode(FORMAT))
    username = connection.recv(1024).decode()
    connection.sendall("password: ".encode(FORMAT))
    password = connection.recv(1024).decode()
    found = False

    #check the existance in the db
    with open(DATABASE_PATH, 'r') as db:
        string_to_prove = username + ',' + password
        line = db.readline()
        while line and not found:
            print(line)
            if string_to_prove in line:
                found = True 
                print("found")
            else :
                line = db.readline()
        if not found:
            connection.sendall("Username or password are not singed...".encode(FORMAT))
    if found:
        DNS[addr] = username
    print(f"DNS: {DNS[addr]}")
    return "/chatroom/" if found else "/"


def broadcast(msg:str, client:socket, addr) ->None:
    for socke in CLIENT_LIST:
        if socke is not client:
            socke.sendall(f"~{DNS[addr]}~ {msg}".encode(FORMAT))

def disconnect(client: socket, addr):
    CLIENT_LIST.remove(client)
    del DNS[addr]


def managing(client: socket, addr):
    #Sendind the message of starting connection
    client.sendall("Create an account or sign in: ".encode(FORMAT))
    answear = client.recv(1024).decode()
    print(answear)
    if answear == '/signin':
        path = '/'
    elif answear == '/login':
        path = '/login/'
    

    if path == '/':
        client.sendall(f"Page: {path} \nSign In Page...\n".encode(FORMAT))
        path = manageStart(client, addr)
    if path == '/login/':
        client.sendall(f"Page {path} \nEnter your credentials...\n".encode(FORMAT))
        path = manageSignIn(client, addr)
    
    if path == '/chatroom/':
        client.sendall(f"Page {path}\nWillkommen im ChatRoom...\n".encode(FORMAT))
        while True:
            msg = client.recv(1024).decode()
            print(msg)
            if(msg == "/quit"):
                client.close()
                CLIENT_LIST.remove(client)
                break
            broadcast(msg, client, addr)
        
    


def driver():
    server = socket(sock.AF_INET, sock.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(10)
    try:
        #Always accept connections 
        while True:
            client, addr = server.accept()
            print(addr)
            CLIENT_LIST.append(client)
            DNS[addr] = "nickname"
            thread = th.Thread(target=managing, args=(client, addr))
            thread.start()
    except KeyboardInterrupt:
        server.close()
        for each in CLIENT_LIST:
            each.close()
        CLIENT_LIST.clear()
        print(f"##############\nThe Server has been closed...")


if __name__ == "__main__":
    driver()