from socket import *
from user import *

from threading import Thread

serversocket = socket(AF_INET,SOCK_STREAM)
HOST = "localhost"
users = []


def main():                         #Need to go to next thread as soon as new connection OR as soon as previous thread is connected

    PORT=12001
    # HOST = "192.168.56.1"
    serversocket.bind((HOST,PORT))
    serversocket.listen(10)

    print("==========SERVER RUNNING AND WAITNG FOR CONNECTIONS==========")
    
    
    while True:                                                                     #Multiple Clients can connect at once (Thread created for each Client)
        connectionSocket, addr = serversocket.accept()
        serverthread = Thread(target=server, args=(connectionSocket,addr))
        serverthread.start()
        print(f"Connected to {addr}")
       

    pool.shutdown(wait=True)
    s.close()

def server(connectionSocket,addr):

    while True:                                                             #While connected?
        try:
            #Receive message from client
            message = connectionSocket.recv(1024).decode()
            print(message)

            #Decision tree // formulate response depending on message received
            command = message[0:message.find("\r")-1]
            message = message [message.find("\n") + 1:]
            if command == "LOGIN":
                returnmessage = login(message,connectionSocket)

            elif command == "GETSTATUS":
                returnmessage = getstatus(message)
            
            elif command == "SETSTATUS":
                setstatus(message)

            elif command == "LIST":
                returnmessage = list_clients()

            elif command == "CHAT":  ######
                
                returnmessage = create_chat(message,addr) ######

            #Send response to client
            print (returnmessage)
            connectionSocket.send(returnmessage.encode())
        except:
            print("Client disconnected. Waiting for reconnect...")
            serversocket.listen(10)
            print("Waiting for connection...")
            connectionSocket, addr = serversocket.accept()
            print(f"Connected to {addr}")
            


def login(message, clientSocket):
    username = message[9:message.find("\r")]      #LOGIN PROTOCOL: "LOGIN " + "\r\n" + "USERNAME " + username + "\r\nPASSWORD " + password+ "\r\nIP NUMBER " + clientSocket.getsockname+"\r\nUDP PORT "+udp_addr + "\r\n\r\n"
    message = message[message.find("\n")+1:]
    password = message[9:message.find("\r")]
    message = message[message.find("\n")+1:]
    ip_num = message[10:message.find("\r")]
    message = message[message.find("\n")+1:]
    udp_addr = (ip_num,int(message[9:message.find("\r")]))

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
                if x.get_udp_addr() != udp_addr:
                    x.set_udp_addr(udp_addr)
            else:
                response =  "UNSUCCESSFUL \r\n" + "PASSWORD \r\n\r\n"
    if found == False :
        users.append(user(username,password,ip_num,udp_addr,"AVAILABLE"))  ######
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
            
    response += "\r\n\r\n"
    return response


def create_chat(message, sender_addr):
    dest_username = message.strip()  #client asking for peer
    chatSocket = socket(AF_INET, SOCK_DGRAM)
    chatSocket.bind((HOST,0))

    sender_user = getCurrentUser(sender_addr[0])

    for user in users:
        if (user.get_username() == dest_username):  
            peer_addr = user.get_udp_addr() ####send request to the user whether peer would like to chat
            if (user.get_status() == 'AWAY' or user.get_status() == 'OFFLINE'):
                return "UNAVAILABLE"
            
            # request = f"CHAT REQUEST \r\n{user.get_username()}={sender_user.get_ip_num()}:{str(sender_user.get_udp_addr()[1])}"
            # chatSocket.sendto(request.encode(), peer_addr)

            return  f"{user.get_username()}={peer_addr[0]}:{peer_addr[1]}"

            
    else:
        return "USER NOT FOUND"


def getCurrentUser(ip_addr):
    for user in users:
        if user.get_ip_num() == ip_addr.strip():
            return user   
    return -1

if __name__ == "__main__":
    main()
    

     
    