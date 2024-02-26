from socket import *
import sys, subprocess



serverName = "192.168.56.1"
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
            else:
                print ("Welcome back {}!".format(username))
            logged_in = True

    print(logged_in)  
    
    


    while logged_in == True:
        
        message = "STATUS \r\nGET\r\n" + "USERNAME " + username +"\r\n\r\n"
        clientSocket.send(message.encode())
        returnmessage = clientSocket.recv(1024).decode()
        print ("Your status is: " + returnmessage[returnmessage.find("\n")+1:]) #Protocol : "STATUS \r\n userstatus\r\n\r\n"
        
        options = "Choose an option:\n1.) Connect to a Client\n2.) List Clients\n3.) Set Status\n4.) Log Out\n5.)Exit\n"              #String of options to be displayed

        user_choice = (input(options))#add all options

        if user_choice == "1":                                  #Enter peer details and then connect with UDP
            peer_username = input("Enter Peer Username:\n")
            ip_address = input("Enter Peer IP Address:\n")


        elif user_choice == "5":                                           #Last option
            exit

        elif user_choice == "4":                                           #Should be second last option
            clientSocket.close()
            logged_in = False
            print("You have been Logged Out.")

        else:
        
            if user_choice == "S":
                newstatus = input("What would you like to set your status to?\n1.) Available\n2.) Away\n")

                if newstatus == "1":
                    message = "STATUS \r\nSET\r\n" + "USERNAME {}\r\n".format(username) +  "AVAILABLE\r\n\r\n"
                elif newstatus == "2":
                    message = "STATUS \r\nSET\r\n" + "USERNAME {}\r\n".format(username) + "AWAY\r\n\r\n"
                else:
                    print("Invalid choice.")

        
            clientSocket.send(message.encode())
            returnmessage = clientSocket.recv(1024)

            
if __name__ == "__main__":
    main()


