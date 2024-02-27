from socket import *
import threading

main_server = socket(AF_INET, SOCK_STREAM)
main_server.connect(("localhost",14000))

user = input("enter user: ")
if (user == 'a'):
    own_port = 12000
    dest_port = 9999
else :
    own_port = 9999
    dest_port = 12000
    
server = socket(AF_INET, SOCK_DGRAM)
server_addr = ("localhost",12000)
# server.bind(server_addr)

def recv_messages():
    while True:
        message, sender = server.recvfrom(1024)
        print(f"{sender} : " + message.decode())

def send_messages():
    while True:
        
        message = input("> ")
        server.sendto(message.encode(), ("localhost",dest_port))


t1 = threading.Thread(target=recv_messages)
t1.start()

t2 = threading.Thread(target=send_messages)
t2.start()