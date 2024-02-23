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
    message = message [message.index("\n") + 1:]
    if command == "LOGIN":
        login(message)
    if command == "STATUS":
        status(message)

    connectionSocket.send(response.encode())

    connectionSocket.close()


def login(message):
    username = message[10:message.index("\r")]      #LOGIN PROTOCOL: "LOGIN " + "\r\n" + "USERNAME " + username.upper() + "\r\nPASSWORD " + password.upper() + "\r\nIP NUMBER " + clientSocket.getsockname + "\r\n\r\n"
    message = message [message.index("\n")+1:]
    password = messasge[10:message.index("\r")]
    message = message [message.index("\n")+1:]
    ip_num = message[11:message.index("\r")]
    found = False
    for x in users:
        if x.get_username == username:          #RESPONSE PROTOCOL: "SUCCESSFUL/UNSUCCESSFUL \r\n" + "REASON \r\n\r\n"
            found = True
            if (x.get_status == "AVAILABLE"):
                response =  "UNSUCCESSFUL \r\n" + "DUPLICATE \r\n\r\n"
            elif x.get_password == password :
                ### SUCCESSFUL LOGIN
                response = "SUCCESSFUL \r\n" + "EXISTING \r\n\r\n"
                if x.get_status != "AWAY":
                    x.set_status("AVAILABLE")
                if x.get_ip_num!=ip_num:
                    x.set_ip_num(ip_num)
            else:
                response =  "UNSUCCESSFUL \r\n" + "PASSWORD \r\n\r\n"
        if found == False :
            users.append(user(username,password,ip_num,"AVAILABLE"))
            response = "SUCCESSFUL \r\n" + "NEW \r\n\r\n"

#Get a user's status or set new status
def status(message):                                # Get Protocol: "STATUS \r\nGET" + "\r\n" + "USERNAME " + username 
    commanddetails = message[:message.index("\r")]
    message = message[message.index("\n")+1:]
    username = message[10:message.index("\r")]
    message = message[message.index("\n")+1:]
    if commanddetails == "GET":
        userstatus = ""
        for x in users:
            if x.get_username == username:
                userstatus = x.get_status()
        if userstatus == "":
            response = "STATUS \r\nDNE\r\n\r\n"
        else:
            response = "STATUS \r\n{}\r\n\r\n".format(userstatus)
    else:                                             # Set Protocol: "STATUS \r\n" + "SET\r\n" + "USERNAME {}\r\n".format(username) + "AVAILABLE\r\n\r\n"
        newstatus = message[:message.index("\r")]
        for x in users:
            if x.get_username==username:
                x.set_status(newstatus)
                
        

     
    

     
    