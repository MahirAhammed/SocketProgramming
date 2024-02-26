from socket import *
from user import *
users = []

def main():
    PORT=12001
    HOST = "192.168.56.1"

    server = socket(AF_INET,SOCK_STREAM)
    server.bind((HOST,PORT))

    server.listen(10)
    print("Waiting for connection...")
    connectionSocket, addr = server.accept()
    print(f"Connected to {addr}")

    while True:                                                             #While connected?
        try:
            #Receive message from client
            message = connectionSocket.recv(1024).decode()
            print(message)

            #Decision tree // formulate response depending on message received
            command = message[0:message.find("\r")-1]
            message = message [message.find("\n") + 1:]
            if command == "LOGIN":
                returnmessage = login(message)

            if command == "STATUS":
                returnmessage = status(message)
            

            if command == "LIST":
                returnmessage = list_clients()

            #Send response to client
            print (returnmessage)
            connectionSocket.send(returnmessage.encode())
        except:
            print("Client disconnected. Waiting for reconnect...")
            server.listen(10)
            connectionSocket, addr = server.accept()
            print(f"Connected to {addr}")


def login(message):
    username = message[9:message.find("\r")]      #LOGIN PROTOCOL: "LOGIN " + "\r\n" + "USERNAME " + username + "\r\nPASSWORD " + password+ "\r\nIP NUMBER " + clientSocket.getsockname + "\r\n\r\n"
    message = message[message.find("\n")+1:]
    password = message[9:message.find("\r")]
    message = message[message.find("\n")+1:]
    ip_num = message[10:message.find("\r")]
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
    return response

#Get a user's status or set new status
def status(message):                                # Get Protocol: "STATUS \r\nGET\r\n" + "USERNAME " + username +"\r\n\r\n"
    commanddetails = message[:message.find("\r")]
    message = message[message.find("\n")+1:]
    username = message[9:message.find("\r")]
    
    if commanddetails == "GET":
        userstatus = ""
        for x in users:
            if x.get_username() == username:
                userstatus = x.get_status()
        if userstatus == "":
            response = "STATUS \r\nDNE\r\n\r\n"
        else:
            response = "STATUS \r\n{}\r\n\r\n".format(userstatus)
    else:                                             # Set Protocol: "STATUS \r\n" + "SET\r\n" + "USERNAME {}\r\n".format(username) + "AVAILABLE\r\n\r\n"
        message = message[message.find("\n")+1:]
        newstatus = message[:message.find("\r")]
        for x in users:
            if x.get_username==username:
                x.set_status(newstatus)
    return response
        

def list_clients():
    response = "LIST \r\n"
    for x in users:
        if (x.get_status != "AWAY"):
            response += x.get_username() + "\r"
            response += x.get_status() + "\r\n"
    response += "\r\n\r\n"
    return response
    

    



if __name__ == "__main__":
    main()
    

     
    