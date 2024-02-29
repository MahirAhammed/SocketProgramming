from socket import *
import sys, subprocess
from threading import Thread


serverName = "196.47.229.247"             # UCT : 196.47.229.247"
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))



def main():
    logged_in = False
    while logged_in == False:
        username = input("Enter Username:\n")
        password = input("Enter Password:\n")
        message = "LOGIN " + "\r\n" + "USERNAME " + username + "\r\nPASSWORD " + password + "\r\nIP NUMBER " + clientSocket.getsockname()[0] + "\r\n\r\n"
        clientSocket.send(message.encode())
        returnmessage = clientSocket.recv(1024).decode()
        #Decision Tree
        returncommand = returnmessage[:returnmessage.find("\r")-1]
        reason = returnmessage[returnmessage.find("\n")+1:-5]

        if returncommand == "UNSUCCESSFUL":
            if reason == "DUPLICATE":                                                       # If user logged in already
                print("User ({}) already logged into the server.".format(username))
            else:                                                                           # If incorrect password
                print("Password incorrect.")
            
        else:                                                                               # If successful - logged_in = True
            if reason == "NEW":
                print ("New user successfully registered.")
                print(clientSocket.getsockname()[1])
            else:
                print ("Welcome back {}!".format(username))
            logged_in = True


    
    


    while logged_in == True:
        
        message = "GETSTATUS \r\n" + "USERNAME " + username +"\r\n\r\n"
        clientSocket.send(message.encode())
        returnmessage = clientSocket.recv(1024).decode()
        print ("Your status is: " + returnmessage[returnmessage.find("\n")+1:]) #Protocol : "STATUS \r\n userstatus\r\n\r\n"
        
    
        options = "Choose an option:\n1.) Chat\n2.) List Clients\n3.) Set Status\n4.) Exit\n"                 #String of options to be displayed
 
        user_choice = (input(options))#add all options

        if user_choice == "1":                                  #Enter peer details and then connect with UDP
            peer_username = input("Enter Peer Username:\n")
            chat(peer_username,username)
            

            


        elif user_choice == "4":                                           #Last option
            message = message = "SETSTATUS \r\n" + "USERNAME {}\r\n".format(username) +  "OFFLINE\r\n\r\n"
            clientSocket.send(message.encode())
            exit()

     
            
        elif user_choice == "3":
            newstatus = input("What would you like to set your status to?\n1.) Available\n2.) Away\n")
            if newstatus == "1":
                message = "SETSTATUS \r\n" + "USERNAME {}\r\n".format(username) +  "AVAILABLE\r\n\r\n"
                clientSocket.send(message.encode())
                returnmessage = clientSocket.recv(1024).decode()
            elif newstatus == "2":
                message = "SETSTATUS \r\n" + "USERNAME {}\r\n".format(username) + "AWAY\r\n\r\n"
                clientSocket.send(message.encode())
                returnmessage = clientSocket.recv(1024).decode()
            else:
                print("Invalid choice.")

        elif user_choice == "2":
            #List clients
            message = "LIST \r\n"
            clientSocket.send(message.encode())
            returnmessage = clientSocket.recv(1024).decode()            #"LIST \r\n" + "username\rstatus\ripaddress\r\n" + ....
            returnmessage = returnmessage[returnmessage.find("\n")+1:]
            client_list = "\t\tLIST OF USERS:\t\nUSERNAME\t"+ "STATUS".ljust(10)+"\tIP ADDRESS\n"
            while (returnmessage!="\r\n\r\n"):             #while not end of the message / list
                client_list += (returnmessage[:returnmessage.find("\r")]).ljust(10)
                returnmessage = returnmessage[returnmessage.find("\r")+1:]
                client_list += "\t{}".format((returnmessage[:returnmessage.find("\r")]).ljust(10))
                returnmessage = returnmessage[returnmessage.find("\r")+1:]
                client_list += "\t{}\n".format(returnmessage[:returnmessage.find("\r")])
                returnmessage = returnmessage[returnmessage.find("\n")+1:]
            print(client_list)
        


    
def listen(sport):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind((serverName, sport))

    while True:
        data = sock.recv(1024)
        print('\rpeer: {}\n> '.format(data.decode()), end='')


def chat(peer_username,username):

    message = "CHAT \r\nSTART\r\n{}\r\n{}\r\n\r\n".format(peer_username,username)
    clientSocket.send(message.encode())

    returnmessage = clientSocket.recv(1024).decode()    
    print(returnmessage)
    command = returnmessage[:returnmessage.find("\r")]

    if command == "BUSY":
        print("User is currently busy.")

    elif command =="AVAILABLE":
        print("User available.")                                        #AVAILABLE\r\npeerIP\r\ndport\r\nsport\r\n\r\n
        returnmessage = returnmessage[returnmessage.find("\n")+1:]
        ip_address = returnmessage[:returnmessage.find("\r")]
        returnmessage = returnmessage[returnmessage.find("\n")+1:]
        dport = returnmessage[:returnmessage.find("\r")]   
        returnmessage = returnmessage[returnmessage.find("\n")+1:]
        sport = returnmessage[:returnmessage.find("\r")]

        print(dport)
        print(sport)

        dport = int(dport)
        sport = int(sport)

        listener = Thread(target=listen(sport), daemon=True)
        listener.start()

        ready = input("Press enter")

        sock = socket(AF_INET, SOCK_DGRAM)  
        sock.bind((serverName, dport))
        sock.sendto(b'0',(ip_address,dport))

        while True:
            msg = input('> ')
            sock.sendto(msg.encode(), (ip_address, dport))

            
if __name__ == "__main__":
    main()


