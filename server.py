from socket import *
from user import *

users = []
PORT=12001
HOST = ''

server = socket(AF_INET,SOCK_STREAM)
server.bind((HOST,PORT))

server.listen(10)
print("Waiting for connection...")

while True:
    connectionSocket, addr = server.accept()
    print(f"Connected to {addr}")

    message = connectionSocket.recv(1024).decode()
    print(message)

    #Decision tree
    command = message[0:message.index("\r")]
    messagecopy = message [message.index("\r"):]
    if command == "LOGIN":
        username = messagecopy[10:messagecopy.index("\r")]
        messagecopy = message [message.index("\r")+1:]
        password = messagecopy[10:messagecopy.index("\r")]
        messagecopy = message [message.index("\r")+1:]
        ip_num = messagecopy[10:messagecopy.index("\r")]
        found - False
        for x in users:
            if x.get_username == username:
                found = True
                if (x.get_status == "AVAILABLE"):
                    ### USER ALREADY LOGGED IN 
                elif x.get_password == password :
                    ### SUCCESSFUL LOGIN
                    # 'YOUR STATUS IS:', then list of options 
                    #if ip address has changed, set to new one
                    # Message
                else:
                    ### INCORRECT PASSWORD
                    # Message
            if found == False :
                users.append(user(username,password,ip_num,"AVAILABLE"))
                # Message
    
    if command == "STATUS":
        username = #PROTOCOL / part of header
        for x in users:
            if x.username == username:
                #return message will have their status



    response = "connected successfully"
    connectionSocket.send(response.encode())

    connectionSocket.close()


     
    