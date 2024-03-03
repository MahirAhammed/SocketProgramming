from socket import *
from threading import Thread
import signal

serverName = "localhost"             # UCT : "196.47.229.247"
serverPort = 12001

serverSocket = socket(AF_INET, SOCK_STREAM)       #Socket for TCP connection with the server
serverSocket.connect((serverName,serverPort))

chatSocket = socket(AF_INET, SOCK_DGRAM)          #Socket for UDP connection with other clients
chatSocket.bind((serverSocket.getsockname()[0],0))  #Default port generated for receiving chats

username=""

def main():
    logged_in = False
    print("==============[WELCOME]==============")
    print("\nEnter QUIT to leave the login screen")
    #Login to server
    while logged_in == False:
        global username
        username = input("Enter Username:\n")

        if (username == 'QUIT'):
            break

        if validateUsername(username) == False:  # checks whether username is valid
            continue

        password = input("Enter Password:\n")
        if (password == 'QUIT'):
            break

        message = "LOGIN " + "\r\n" + "USERNAME " + username + "\r\nPASSWORD " + password+ "\r\nIP NUMBER " + serverSocket.getsockname()[0] + "\r\nSOCKET NUMBER " + str(chatSocket.getsockname()[1]) + "\r\n\r\n"

        serverSocket.send(message.encode())            #Send login request to server
        response = serverSocket.recv(1024).decode()     # response from server regarding login

        feedback = response[:response.find("\r")-1]     #Extract server feedback to determine what action to take
        reason = response[response.find("\n")+1:-5]      # Extract the reason for above feedback                                 

        if feedback == "UNSUCCESSFUL":
            if reason == "DUPLICATE":                                                   # If user logged in already
                print(f"\nYou are already logged into the server.\n")
                logged_in = True
            else:                                                                       # If incorrect password
                print("\nIncorrect password.\n")
            
        else:                                                               # Successful login
            if reason == "NEW":                                             # New user
                print ("\nYou are successfully registered.\n")
            else:                                                           # Existing user
                print (f"\nWelcome back {username}!\n")
            logged_in = True

    # Main menu
    while logged_in == True:
        try:
                
            message = "GETSTATUS \r\n" + "USERNAME " + username +"\r\n\r\n"  # Protocol to get current status of user
            serverSocket.send(message.encode())                              # Request to server
            response = serverSocket.recv(1024).decode()                     #Response from server
            print ("Your Status: " + response[response.find("\n")+1:])     #Protocol : "STATUS \r\n userstatus\r\n\r\n"
            
            #String of options to be displayed
            prompt = "Choose an option:\n[1] Chat\n[2] Show Clients List\n[3] Set Status\n[4] Log out\n"  
    
            user_choice = (input(prompt))

            if user_choice == "1":                    
                # Chat with a specified user (they will not receive messages unless they choose to chat with you as well)
                print(f"\n~~~~~~~Received messages~~~~~~~\n")

                chatSocket.settimeout(1)  # 2 seconds timeout where the program checks whether any messages were received from peers
                print("\nLooking for messages...\n")
                try:
                    # Attempt to receive data
                    data, _ = chatSocket.recvfrom(1024)
                    print("\n---MESSAGE FROM---")
                    print(data.decode())
                    

                except timeout:
                    # Handle timeout exception
                    print("No messages received")

                except KeyboardInterrupt:
                    pass
                    

                print("\n**********[Chat Space]**********\n")

                peer_username = input("Enter Peer Username:\n")
                chat(peer_username)  

                message = f"SETSTATUS \r\nUSERNAME {username}\r\AVAILABLE\r\n\r\n"              #Set user status back to Available once they have finished chatting
                serverSocket.send(message.encode())
                response = serverSocket.recv(1024).decode()
                
                
            elif user_choice == "2":                            # List clients
                message = "LIST \r\n"                           # Send request to server
                serverSocket.send(message.encode())             # server reponse
                response = serverSocket.recv(1024).decode()                                        #RETURN PROTOCOL: "LIST \r\n" + "username\rstatus\r\n" + ....
                response = response[response.find("\n")+1:]
                client_list = "\tLIST OF USERS:\t\nUSERNAME\t\t"+ "STATUS".ljust(20) + "\t\n"             # list all users and their statuses except for users with status set as AWAY
                client_list +='___________________________________\n'

                while (response!="\r\n\r\n"):                               #while not end of the message / list
                    # Extracts username as formats to left for displaying purposes
                    client_list += (response[:response.find("\r")]).ljust(20)
                    response = response[response.find("\r")+1:]

                    # Extracts user statuses and formats it for displaying purposes
                    client_list += "\t{}\n".format((response[:response.find("\r")]).ljust(20))
                    response = response[response.find("\n")+1:]

                print(client_list)

                
            elif user_choice == "3":     # Set status to Available or Away (other statuses cannot be set by user [BUSY(chatting) and OFFLINE])
                newstatus = input("Set your status?\n[1] Available\n[2] Away\n")
                if newstatus == "1":
                    message = f"SETSTATUS \r\nUSERNAME {username}\r\nAVAILABLE\r\n\r\n"
                    serverSocket.send(message.encode())
                    response = serverSocket.recv(1024).decode()      #response is just "DONE" (to ensure synchronization) as status is shown each time the menu is printed
                elif newstatus == "2":
                    message = f"SETSTATUS \r\nUSERNAME {username}\r\nAWAY\r\n\r\n"
                    serverSocket.send(message.encode())
                    response = serverSocket.recv(1024).decode()
                else:
                    print("Invalid choice.\n")

            
            elif user_choice == "4":                 # Disconnect from server and close client program
                message = message = "SETSTATUS \r\n" + "USERNAME {}\r\n".format(username) +  "OFFLINE\r\n\r\n"
                serverSocket.send(message.encode())
                serverSocket.close()
                print("Logging out....")
                exit()

        except KeyboardInterrupt:
            print("Leaving program.....")

def validateUsername(username):
    
    invalid_Names = ["LOGIN", "GETSTATUS", "SETSTATUS", "SOCKET", "UDP", "TCP", "AVAILABLE", "BUSY", "OFFLINE", "ONLINE","DNE"]

    if username.strip().upper() in invalid_Names:        # if username any of the invalid names in the list
        print("========!!! Invalid username, username clashes with protocols !!!==========")
        return False
    
    elif username.isalnum() == False:                    # if username contains any character beside numbers and letters
        print("=======!!! Username cannot contain special characters including space !!!=======")
        return False
    return True 


#Handles chat request from user
def chat(peer_username):
    message = "CHAT \r\nSTART\r\n{}\r\n\r\n".format(peer_username)           #Message to server requesting chat information
    serverSocket.send(message.encode())
    response = serverSocket.recv(1024).decode()                 #Chat info of peer status, ip and port for udp
    command = response[:response.find("\r")]

    if command == "BUSY":
        print("User is currently busy.\n")
    
    elif command == "OFFLINE":
        print("User is currently offline.\n")

    elif command == "DNE":
        print("User does not exist.\n")

    elif command =="AVAILABLE":
        print("User available. Initializing chat...\n\n(To quit a chat at any time, type QUIT and press enter.)\n")                                        #AVAILABLE\r\npeerIP\r\npeerPort\r\n\r\n
        response = response[response.find("\n")+1:]
        ip_address = response[:response.find("\r")]
        response = response[response.find("\n")+1:]
        peer_port = int(response[:response.find("\r")])
        
        chat_thread = Thread(target=chat_session, args=(ip_address,peer_port,),daemon=True)                     #Thread for chatting
        chat_thread.start()
        chat_thread.join()
        

        message = "SETSTATUS \r\n" + "USERNAME {}\r\n".format(username) +  "AVAILABLE\r\n\r\n"              #Set user status back to Available once they have finished chatting
        serverSocket.send(message.encode())
        returnmessage = serverSocket.recv(1024).decode()

        chatSocket = socket(AF_INET, SOCK_DGRAM)   
        chatSocket.bind((serverSocket.getsockname()[0],0))
        message = "SOCKET \r\n{}\r\n{}\r\n\r\n".format(username,chatSocket.getsockname()[1])
        serverSocket.send(message.encode())
        returnmessage = serverSocket.recv(1024).decode()

# creates chat session when requested to chat
def chat_session(peer_ip,peer_port):
    
    try:
        recv_thread = Thread(target=recv_messages)                                      #Thread for receiving messages
        recv_thread.start()
        send_messages(peer_ip,peer_port)                                                #Sending executed on the chat thread (not the main thread)
        recv_thread.join()
        return
    
    except:                                                                             
        print("Peer Disconnected. Press enter to continue...")
        return
     
#Receive messages from peers
def recv_messages():
    
    connected = False
    try:
        while True:
            data, _ = chatSocket.recvfrom(1024)
            data = data.decode()
            peer_username = data[0: data.find(":")]
            if connected==False:                       #Once user receives first message, their status is set to "BUSY"
                connected=True
                message = "SETSTATUS \r\n" + "USERNAME {}\r\n".format(username) +  "BUSY\r\n\r\n"   
                serverSocket.send(message.encode())
                returnmessage = serverSocket.recv(1024).decode()
                
            if data == 'QUIT':                    #If peer "QUIT", chat is closed
                print(f"{peer_username} has left the chat. Press enter to continue...")
                chatSocket.close()
                return
            
            print(f"{data}\n", end='')
    except:
        return
    
# Sends messages to peer
def send_messages(peer_ip,peer_port):
    try:
        
        while True:
            message = input('> ')
            chatSocket.sendto(f"{username}: {message}".encode(),(peer_ip, peer_port))
            if message == 'QUIT':                  #In order to leave a chat, user types "QUIT"
                print("Disconnected from chat.\n")

                setStatus = f"SETSTATUS \r\nUSERNAME {username}\r\AVAILABLE\r\n\r\n"              #Set user status back to Available once they have finished chatting
                serverSocket.send(setStatus.encode())
                response = serverSocket.recv(1024).decode()
                chatSocket.close()

                return    
    except:
        return


if __name__ == "__main__":
    main()