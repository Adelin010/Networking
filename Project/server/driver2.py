import socket as sock
from socket import socket
from threading import Thread
from server_infos import *
from server_infos import _Addr, _nickname, _routing_path
from time import sleep
# DataBase Interface functions
# For adding and searching --> later: deleting 
def searchToken(username: str, password:str) -> str:
    return username + ',' + password

def checkInDB(string:str):
    
    with open(DATABASE_PATH, 'r') as db:
        for line in db.readlines():
            if string in line : return True 
    return False


def appendInDB(string:str) -> None:
    with open(DATABASE_PATH, 'a') as db:
        db.write('\n'+string)

# Database management util functions
def auth(username: str, password: str) -> bool:
    return checkInDB(searchToken(username, password))

# returns 1 if the user is new and it was added into the database
# otherwise 0 if there is a user in the DB
def addInDB(username: str, password: str) -> int:
    token = searchToken(username, password)
    if not checkInDB(token):
        appendInDB(token)
        return 1 
    return 0


# Connection & Socket-related util functions
def sendMsg(client: socket, string:str)-> None:
    try:
        client.sendall(string.encode(FORMAT))
    except :
        print("\033[31mError occured at sending message \033[0m")

def getMsg(client:socket) -> str:
    return client.recv(BUF).decode()

def disconnectClient(client: socket, addr: _Addr):
    #send a message to all the others users in the room
    broadcast(client, addr ,f"\033[32m{DNS[addr][0]} has disconnect...\033[0m")
    #Remove the client in cause
    CLIENT_LIST.remove(client)
    del DNS[addr]
    client.close()

def disconnectServer(server: socket):
    for client in CLIENT_LIST:
        client.close()
    CLIENT_LIST.clear()
    DNS.clear()
    THREADS.clear()
    server.close()

# Setting the DNS name of the client to the default nickname
# Adding the client to the connections
def addConnection(client: socket, addr: _Addr, client_thread: th.Thread):
    print(f"\033[32mThe client {addr} is connected... \033[0m")
    CLIENT_LIST.append(client)
    DNS[addr] = ("nickname", '/')
    THREADS.append(client_thread)

def getConnection(server: socket) -> tuple[socket, _Addr, th.Thread]:
    client, addr = server.accept()
    client_thread = Thread(target=inputClient, args=(client, addr), daemon=True)
    # Before starting the process the server must send the options
    addConnection(client, addr, client_thread)
    wellcomePage(client, addr)
    return (client, addr, client_thread)


def broadcast(client: socket,addr: _Addr , message: str) -> None:
    for conn in CLIENT_LIST:
        if client != conn and DNS[addr][1] == "/chatroom":
            sendMsg(conn, f"${DNS[addr][0]}$ {message}")


def wellcomePage(client: socket, addr: _Addr):
    sendMsg(client, f"-> Current Page: {DNS[addr][1]}\nSwitch between pages\n\033[32m/signin\033[0m to registrate\n\033[32m/login\033[0m to authentificate\n\033[32m/quit\033[0m for closing the session\033[0m\nyour choice: ")
    option = getMsg(client)
    routing(client, addr, option)
    

def routing(client: socket, addr: _Addr ,route: str, message:str = ''):
    #Change to the current path
    DNS[addr] = (DNS[addr][0], route)
    match route:
        case "/":
            wellcomePage(client, addr)
        case "/signin":
            signInPage(client, addr)
        case "/login":
            logInPage(client, addr)
        case "/chatroom":
            chatRoom(client, addr, message)
        case "/quit":
            disconnectClient(client, addr)
        case _:
            errorPage(client, addr)


def signInPage(client: socket, addr: _Addr = None):
    #Get the username and the password
    sleep(.5)
    sendMsg(client, f"->Current Page: {DNS[addr][1]}\n Sing in with a username and a password\n\033[32m     username: \033[0m")
    username = getMsg(client)
    sendMsg(client, f"\033[32m     password: \033[0m")
    password = getMsg(client)
    response_db: int = addInDB(username, password)
    sleep(.5)
    #Check in which case is the current user
    if response_db == 1:
        #DNS name must be updated
        sendMsg(client, "   \033[32m!New Account added...\033[0m")
    elif response_db == 0:
        sendMsg(client, "   \033[32m!User already registrated\033[0m")
    #Go back to the starting Page and send the new Path
    sendMsg(client, '/')
    routing(client, addr, '/')

def logInPage(client: socket, addr: _Addr = None):
    sleep(.5)
    sendMsg(client, f"->Current Page: {DNS[addr][1]}\n Enter your credentials\n\033[32m     username: \033[0m")
    username = getMsg(client)
    sendMsg(client, f"\033[32m     password: \033[0m")
    password = getMsg(client)
    sleep(.5)
    if auth(username, password):
        DNS[addr] = (username, DNS[addr][1])
        sendMsg(client, "   \033[32m Logged In Successfully...\033[0m")
        routing(client, addr, '/chatroom')

    else:
        sendMsg(client, "   \033[32m Credentials are not matched...\033[0m")
        sendMsg(client, '/')
        routing(client, addr, '/')

  
def errorPage(client: socket, addr: _Addr = None):
    sendMsg(client, f"  \033[32m Current Page {DNS[addr][1]} does not exist...\033[0m")
    sleep(1)
    routing(client, addr, '/')

def chatRoom(client: socket, addr: _Addr, message: str):
    if message != '':
        broadcast(client,addr ,message)

# Separate function executed in the thread so thus it will not 
# halt the main one - which has the task to obtain incoming connections
def inputClient(client: socket, addr: _Addr):

    while True:
        message = getMsg(client)
        # Generical path change
        if message == "/quit":
            disconnectClient(client, addr)
            break
        else:
            chatRoom(client, addr, message)

    # If out of the loop the thread must join and stop
    index = CLIENT_LIST.index(client)
    client_thread = THREADS[index]
    client_thread.join()
    THREADS.remove(client_thread)
def run():
    server = socket(sock.AF_INET, sock.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(100)
    try:
        #Main Thread used to accept connections
        while True:
            client, addr, thread = getConnection(server)
            thread.start()
            print("Thread starts>>>")
    except KeyboardInterrupt:
        disconnectServer(server)
        print("\n\033[32m Server closed... \033[0m")



if __name__ == "__main__":
    run()