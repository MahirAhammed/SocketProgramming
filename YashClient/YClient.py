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
    message = "LOGIN " + "\r\n" + "USERNAME " + username.upper() + "\r\nPASSWORD " + password.upper() + "IP NUMBER " + clientSocket.getsockname + "\r\n\r\n"
    clientSocket.send(message.encode())
    returnmessage = clientSocket.recv(1024)
    #Decision Tree
    # If incorrect password
    # If user logged in already
    # If successful - logged_in = True


while logged_in == True:
    clear_screen()  #clear terminal
    message = "STATUS " + "\r\n" + "USERNAME " + username 
    clientSocket.send(message.encode())
    returnmessage = clientSocket.recv(1024)
    print ("Your status is: " + returnmessage[]) #DECIDE ON PROTOCOL FOR THIS 
    
    user_choice = (raw_input("Choose an option:\n")).upper() #add all options

    if user_choice == "D":
        clientSocket.close()
        print("You have been Disconnected.")

    if user_choice == "Q":
        exit

    if user_choice == "S":
        #CHANGE STATUS
        #CLEAR THE LIST etc. every time



        



