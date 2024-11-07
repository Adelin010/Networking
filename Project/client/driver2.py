import socket as sock
from socket import socket
from threading import Thread

#get the ip addres and the port
SERVER = "127.0.1.1"
PORT = 9898
ADDR = (SERVER, PORT) 
FORMAT = 'utf-8'
BUF = 1024


#util functions
def sendMsg(client: socket, string:str)-> None:
    try:
        client.sendall(string.encode(FORMAT))
    except :
        print("\033[31mError occured at sending message \033[0m")


def getMsg(client:socket) -> str:
    return client.recv(BUF).decode()

#pages functions 

def StartingPage(connection: socket) -> str:
    choice = input(getMsg(connection))
    sendMsg(connection, choice)
    return choice

def manageCredentialPage(connection: socket) -> str:
    #Username 
    username  = input(getMsg(connection))
    sendMsg(connection, username)
    #Password
    password = input(getMsg(connection))
    sendMsg(connection, password)
    # Get the result message
    print(getMsg(connection))
    #return the new path
    return "/chatroom"

def readInChat(connection: socket):
    while True:
        try:
            message = getMsg(connection)
            print(message)
        except:
            print("\033[31m Error when receiving the message from the server \033[0m")
            connection.close()
            break

def writeInChat(connection: socket):
    while True:
        message = input('~')
        if message == "/quit":
            sendMsg(connection, message)
            connection.close()
            print("connection closed...")
            break
        sendMsg(connection, message)



def run():
    conn = socket(sock.AF_INET, sock.SOCK_STREAM)
    conn.connect(ADDR)
    path = '/'
    try:
        while True and path != "/chatroom" or path != "/quit":
            if path == '/':
                path = StartingPage(conn)
                print(f"Path after the StartingPage: {path}")
            elif path == "/signin" or path == "/login":
                print(f"Path before login: {path}")
                path = manageCredentialPage(conn)
                print(f"Path after login: {path}")
            elif path == "/chatroom":
                print("In chatRoom")
                th1 = Thread(target=writeInChat, args=(conn,))
                th1.start()
                th2 = Thread(target = readInChat, args=(conn,))
                th2.start()
                break
            elif path == "/quit":
                conn.close()
                print("connection closed...")
                break
            else:
                print(getMsg(conn))
                path = '/'

    except KeyboardInterrupt:
        conn.close()
        print("\033[31m Client is out...\033[0m")



if __name__ == "__main__":
    run()