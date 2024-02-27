from socket import *
from user import *

from threading import Thread

users = []

def main():                         

    PORT=12001
    HOST = "192.168.3.75"    # UCT : 196.47.229.247"
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
            #Receive message from client
            message = connectionSocket.recv(1024).decode()
            print(message)

            #Decision tree // formulate response depending on message received
            command = message[0:message.find("\r")-1]
            message = message [message.find("\n") + 1:]
            if command == "LOGIN":
                returnmessage = login(message)

            elif command == "GETSTATUS":
                returnmessage = getstatus(message)
            
            elif command == "SETSTATUS":
                setstatus(message)

            elif command == "LIST":
                returnmessage = list_clients()

            #Send response to client
            print (returnmessage)
            connectionSocket.send(returnmessage.encode())
        except:
            break
            


def login(message):
    username = message[9:message.find("\r")]      #LOGIN PROTOCOL: "LOGIN " + "\r\n" + "USERNAME " + username + "\r\nPASSWORD " + password+ "\r\nIP NUMBER " + clientSocket.getsockname + "\r\n\r\n"
    message = message[message.find("\n")+1:]
    password = message[9:message.find("\r")]
    message = message[message.find("\n")+1:]
    ip_num = message[10:message.find("\r")]
    found = False
    for x in users:
        if x.get_username() == username:          #RESPONSE PROTOCOL: "SUCCESSFUL/UNSUCCESSFUL \r\n" + "REASON \r\n\r\n"
            found = True
    
            if (x.get_status() == "AVAILABLE"):
                response =  "UNSUCCESSFUL \r\n" + "DUPLICATE \r\n\r\n"
            elif x.get_password() == password :
                ### SUCCESSFUL LOGIN
                response = "SUCCESSFUL \r\n" + "EXISTING \r\n\r\n"
                if x.get_status() != "AWAY":
                    x.set_status("AVAILABLE")
                if x.get_ip_num()!=ip_num:
                    x.set_ip_num(ip_num)
            else:
                response =  "UNSUCCESSFUL \r\n" + "PASSWORD \r\n\r\n"
    if found == False :
        users.append(user(username,password,ip_num,"AVAILABLE"))
        response = "SUCCESSFUL \r\n" + "NEW \r\n\r\n"
    return response

#Get a user's status or set new status
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

def setstatus(message):                                    # Set Protocol: "SETSTATUS \r\n" +  "USERNAME {}\r\n".format(username) + "AVAILABLE\r\n\r\n"
    username = message[9:message.find("\r")]
    message = message[message.find("\n")+1:]
    newstatus = message[:message.find("\r")]
    for x in users:
        if x.get_username()==username:
            x.set_status(newstatus)
        
        

def list_clients():
    response = "LIST \r\n"
    for x in users:
        if (x.get_status != "AWAY"):
            response += x.get_username() + "\r"
            response += x.get_status() + "\r"
            response += x.get_ip_num() + "\r\n"
    response += "\r\n\r\n"
    return response
    



if __name__ == "__main__":
    main()
    

     
    