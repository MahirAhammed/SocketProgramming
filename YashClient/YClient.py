from socket import *
import sys, subprocess
logged_in = False

def clear_screen():
    operating_platform = sys.platform

    if operating_platform == "win32":
        subprocess.run("cls", shell=True)
    elif operating_platform == "linux":
        subprocess.run("clear", shell=True)




serverName = ""
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

while logged_in == False:
    username = raw_input("Enter Username:\n")
    password = raw_input("Enter Password:\n")
    message = "LOGIN " + "\r\n" + "USERNAME " + username.upper() + "\r\nPASSWORD " + password.upper() + "\r\nIP NUMBER " + clientSocket.getsockname + "\r\n\r\n"
    clientSocket.send(message.encode())
    returnmessage = clientSocket.recv(1024)
    #Decision Tree
    returncommand = returnmessage[0:returnmessage.index("\r")]
    reason = returnmessage[returnmessage.index("\n")+1:]

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
    
   
   


while logged_in == True:
    
    message = "STATUS \r\nGET\r\n" + "\r\n" + "USERNAME " + username 
    clientSocket.send(message.encode())
    returnmessage = clientSocket.recv(1024)
    print ("Your status is: " + returnmessage[returnmessage.index("\n")+1:]) #Protocol : "STATUS \r\n userstatus\r\n\r\n"
    
    options = "Choose an option:\n1.) \n2.) \n3.) \n4.) \n5.)"              #String of options to be displayed

    user_choice = (raw_input(options)).upper() #add all options

    if user_choice == "":                                           #Should be second last option
        clientSocket.close()
        print("You have been Disconnected.")

    if user_choice == "":                                           #Last option
        exit

    if user_choice == "S":
        newstatus = raw_input("What would you like to set your status to?\n1.) Available\n2.) Away\n")

        if newstatus == "1":
            message = "STATUS \r\nSET\r\n" + "USERNAME {}\r\n".format(username) +  "AVAILABLE\r\n\r\n"
        elif newstatus == "2":
            message = "STATUS \r\nSET\r\n" + "USERNAME {}\r\n".format(username) + "AWAY\r\n\r\n"
        else:
            print("Invalid choice.")

   
    clientSocket.send(message.encode())
    returnmessage = clientSocket.recv(1024)

        



