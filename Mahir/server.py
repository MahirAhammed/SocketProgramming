from socket import *
import threading

main_server = socket(AF_INET, SOCK_STREAM)
main_server.bind(('',14000))
main_server.listen()

clients = []

server = socket(AF_INET, SOCK_DGRAM)

def handle_chat():

    while True:

        message, sender = server.recvfrom(1024)
        print(f"{sender} : " + message.decode())

def handle_server():
   while True:
        client_socket, client_address = main_server.accept()
        print(f"Connected: {client_address}")
        clients.append((client_socket,client_address))



def main():
    t1 = threading.Thread(target=handle_server)
    t1.start()

    t2 = threading.Thread(target=handle_chat)
    t2.start()


if __name__ =='__main__':
    main()