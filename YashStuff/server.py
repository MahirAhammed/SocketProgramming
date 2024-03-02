from socket import *
from user import *

from threading import Thread

users = []

def main():                         

    PORT=12001
    HOST = ""    # UCT : 196.47.229.247"
    serversocket = socket(AF_INET,SOCK_STREAM)
    serversocket.bind((HOST,PORT))
    serversocket.listen(10)

    print("Waiting for connection...")
    
    
    while True:                                                                     #Multiple Clients can connect at once (Thread created for each Client)
        connectionSocket, addr = serversocket.accept()
        serverthread = Thread(target=server, args=(connectionSocket,addr))
        serverthread.start()
        print(f"Connected to {addr}")
       

   
def server(connectionSocket,addr):

    while True:                                                             
        try:
            message = connectionSocket.recv(1024).decode()                              #Receive message from client

            #Decision tree // formulate response depending on message received
            command = message[0:message.find("\r")-1]
            message = message [message.find("\n") + 1:]
            
            if command == "LOGIN":
                returnmessage = login(message)

            elif command == "GETSTATUS":
                returnmessage = getstatus(message)
            
            elif command == "SETSTATUS":
                returnmessage = setstatus(message)

            elif command == "LIST":
                returnmessage = list_clients()

            elif command == "CHAT":
                returnmessage = chat(message)

            elif command == "SOCKET":
                returnmessage = set_socket(message)

            
            print (returnmessage)
            connectionSocket.send(returnmessage.encode())                               #Send response to client
        except:
            break
            

#Log user in to the server
def login(message):
    username = message[9:message.find("\r")]      #LOGIN PROTOCOL: "LOGIN " + "\r\n" + "USERNAME " + username + "\r\nPASSWORD " + password+ "\r\nIP NUMBER " + clientSocket.getsockname + "\r\nSOCKET NUMBER " + str(clientSocket.getsockname()[1]) + "\r\n\r\n"
    message = message[message.find("\n")+1:]
    password = message[9:message.find("\r")]
    message = message[message.find("\n")+1:]
    ip_num = message[10:message.find("\r")]
    message = message[message.find("\n")+1:]
    sock_num = message[14:message.find("\r")]
    
    found = False
    for x in users:
        if x.get_username() == username:          #RESPONSE PROTOCOL: "SUCCESSFUL/UNSUCCESSFUL \r\n" + "REASON \r\n\r\n"
            found = True
    
            if (x.get_status() == "AVAILABLE"):                                         #User is already logged into the server
                response =  "UNSUCCESSFUL \r\n" + "DUPLICATE \r\n\r\n"
            elif x.get_password() == password :                                         #SUCCESSFUL LOGIN
                response = "SUCCESSFUL \r\n" + "EXISTING \r\n\r\n"
                if x.get_status() != "AWAY":
                    x.set_status("AVAILABLE")
                if x.get_ip_num()!=ip_num:                                              #Update ip number and chat port number if they have changed since last login
                    x.set_ip_num(ip_num)
                if x.get_sock_num()!=sock_num:
                    x.set_sock_num(sock_num)    
            else:
                response =  "UNSUCCESSFUL \r\n" + "PASSWORD \r\n\r\n"
    if found == False :                                                                 #If user does not exist, create new user
        users.append(user(username,password,ip_num,sock_num,"AVAILABLE"))
        
        response = "SUCCESSFUL \r\n" + "NEW \r\n\r\n"
    return response

#Get a user's status 
def getstatus(message):                                # Get Protocol: "GETSTATUS \r\n" + "USERNAME " + username +"\r\n\r\n"
    username = message[9:message.find("\r")]
    userstatus = ""
    for x in users:
        if x.get_username() == username:
            userstatus = x.get_status()
    if userstatus == "":
        response = "STATUS \r\nDNE\r\n\r\n"
    else:
        response = "STATUS \r\n{}\r\n\r\n".format(userstatus)
    return response

#Set user's status
def setstatus(message):                                    # Set Protocol: "SETSTATUS \r\n" +  "USERNAME {}\r\n".format(username) + "AVAILABLE\r\n\r\n"
    username = message[9:message.find("\r")]
    message = message[message.find("\n")+1:]
    newstatus = message[:message.find("\r")]
    for x in users:
        if x.get_username()==username:
            x.set_status(newstatus)
            print(x.get_status())       ###
    response = "DONE"   
    return response
        
        
#return a list of clients (Available, Offline and Busy) and their statuses
def list_clients():
    response = "LIST \r\n"
    for x in users:
        if (x.get_status() != "AWAY"):
            response += x.get_username() + "\r"
            
            response += x.get_status() + "\r\n"
            
    response += "\r\n\r\n"
    return response                                             #Response Protocol: "LIST \r\n" + "username\rstatus\r\n" + ....
    

def chat(message):
    command =  message[:message.find("\r")]                     #Protocol: "CHAT \r\nSTART\r\n{}\r\n{}\r\n\r\n".format(peer_username,own_username)
    message = message[message.find("\n")+1:]
    peer_username = message[:message.find("\r")]
    message = message[message.find("\n")+1:]
    username = message[:message.find("\r")]
    print (command)
    if command == "START":
        response = "DNE\r\n\r\n"
        for x in users:
            if peer_username == x.get_username():
                status = x.get_status()
                if (status == "BUSY") or (status=="AWAY"):
                    response = "BUSY\r\n\r\n"
                elif status == "OFFLINE":
                    response = "OFFLINE\r\n\r\n"
                else:        
                    response = "AVAILABLE\r\n{}\r\n{}\r\n\r\n".format(x.get_ip_num(),x.get_sock_num())              #If peer is available, Response Protocol: "AVAILABLE\r\npeerIP\r\npeerPort\r\n\r\n"
    return response
                    

def set_socket(message):                                                                    #Set user's stored UDP port number to new value
    username = message[:message.find("\r")]
    message = message[message.find("\n")+1:]
    newsocket = message[:message.find("\r")]

    for x in users:
        if x.get_username() == username:
            x.set_sock_num(newsocket)
    return "DONE"


                



if __name__ == "__main__":
    main()
    
