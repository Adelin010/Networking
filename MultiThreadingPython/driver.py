import socket as sock
import threading as th


PORT = 6457
SERVER = sock.gethostbyname(sock.gethostname())
print(SERVER)
HEADER = 64
FORMAT = 'utf-8'

ADDR = (SERVER, PORT)


server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
server.bind(ADDR)


client_list = []


def remove_client(client):
    if client in client_list:
        client_list.remove(client)

def broadcast(msg, connection):
    for client in client_list:
        if client != connection:
            try: 
                client.send(msg.encode(FORMAT))
            except: 
                remove_client(client)

def income_clients(conn: sock, addr):
    print(f"New Connection established for {addr}")
    connected = True
    while connected :
        msg_len = conn.recv(HEADER).decode(FORMAT)
        if msg_len:
            msg_len = int(msg_len)
            msg = conn.recv(msg_len).decode(FORMAT)
            print(f"{addr}: {msg}")
            conn.send("MSG RECIEVED".encode(FORMAT))
            if msg == "#DIS":
                connected = False
            mess = "<"+str(addr)+">: " + msg
            broadcast(mess, conn)

    conn.close()

def main():
    server.listen()
    print(f"Server starting listening on {SERVER}... ")
    while True:
        conn, addr = server.accept()
        tr = th.Thread(target=income_clients, args=(conn, addr))
        client_list.append(conn)
        tr.start()
        print(f"No of clients: {th.active_count() - 1}")
    server.close()

print("Server Programm has starting...")
main()