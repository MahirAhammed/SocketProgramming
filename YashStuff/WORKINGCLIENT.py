from socket import *
from threading import Thread


serverName = "localhost"             # UCT : "196.47.229.247"
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_STREAM)                         #Socket for TCP connection with the server
clientSocket.connect((serverName,serverPort))

chatSocket = socket(AF_INET, SOCK_DGRAM)                            #Socket for UDP connection with other clients
chatSocket.bind((clientSocket.getsockname()[0],0))

username=""

bank = "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz,\'\"?!.$*&_0123456789"        #Global bank variable for encrypting and decrypting messages

def main():
    logged_in = False
    while logged_in == False:
        global username
        username = input("Enter Username:\n")
        password = input("Enter Password:\n")
        message = "LOGIN " + "\r\n" + "USERNAME " + username + "\r\nPASSWORD " + password+ "\r\nIP NUMBER " + clientSocket.getsockname()[0] + "\r\nSOCKET NUMBER " + str(chatSocket.getsockname()[1]) + "\r\n\r\n"

        clientSocket.send(message.encode())                                                         #Send login request with above details 
        returnmessage = clientSocket.recv(1024).decode()
        returncommand = returnmessage[:returnmessage.find("\r")-1]
        reason = returnmessage[returnmessage.find("\n")+1:-5]                                       

        if returncommand == "UNSUCCESSFUL":
            if reason == "DUPLICATE":                                                               # If user logged in already
                print("\nUser ({}) already logged into the server.\n".format(username))
            else:                                                                                   # If incorrect password
                print("\nPassword incorrect.\n")
            
        else:                                                                                       # Successful login
            if reason == "NEW":                                                                     #New user
                print ("\nNew user successfully registered.\n")
            else:                                                                                   #Existing user
                print ("\nWelcome back {}!\n".format(username))
            logged_in = True



    while logged_in == True:
        
        print("Current User: {}\n".format(username))
        message = "GETSTATUS \r\n" + "USERNAME " + username +"\r\n\r\n"
        clientSocket.send(message.encode())
        returnmessage = clientSocket.recv(1024).decode()
        print ("Current Status: " + returnmessage[returnmessage.find("\n")+1:])                     #Protocol : "STATUS \r\n userstatus\r\n\r\n"
        
    
        options = "Choose an option:\n1.) Chat\n2.) List Clients\n3.) Set Status\n4.) Exit\n"       #String of options to be displayed
 
        user_choice = (input(options))

        if user_choice == "1":                                                                      #Chat with a specified user (they will not receive messages unless they choose to chat with you as well)
            global peer_username
            peer_username = input("Enter Peer Username:\n")
            print("\n")
            chat(peer_username,username)            

        elif user_choice == "2":                                                                    #List clients
            message = "LIST \r\n"
            clientSocket.send(message.encode())
            returnmessage = clientSocket.recv(1024).decode()                                        #RETURN PROTOCOL: "LIST \r\n" + "username\rstatus\r\n" + ....
            returnmessage = returnmessage[returnmessage.find("\n")+1:]
            client_list = "\tLIST OF USERS:\t\nUSERNAME\t"+ "STATUS".ljust(10) + "\t\n"             #Will only list usernames and statuses of Available, Busy (chatting) and Offline users
            while (returnmessage!="\r\n\r\n"):                                                      #while not end of the message / list
                client_list += (returnmessage[:returnmessage.find("\r")]).ljust(10)
                returnmessage = returnmessage[returnmessage.find("\r")+1:]

                client_list += "\t{}\n".format((returnmessage[:returnmessage.find("\r")]).ljust(10))
                returnmessage = returnmessage[returnmessage.find("\n")+1:]

                
            print(client_list)
        

     
            
        elif user_choice == "3":                                                                                #Set status to Available or Away (other statuses cannot be set by user [BUSY(chatting) and OFFLINE])
            newstatus = input("What would you like to set your status to?\n1.) Available\n2.) Away\n")
            if newstatus == "1":
                message = "SETSTATUS \r\n" + "USERNAME {}\r\n".format(username) +  "AVAILABLE\r\n\r\n"
                clientSocket.send(message.encode())
                returnmessage = clientSocket.recv(1024).decode()                                                #return message is just "DONE" (to ensure synchronization) as status is shown each time the menu is printed
            elif newstatus == "2":
                message = "SETSTATUS \r\n" + "USERNAME {}\r\n".format(username) + "AWAY\r\n\r\n"
                clientSocket.send(message.encode())
                returnmessage = clientSocket.recv(1024).decode()
            else:
                print("Invalid choice.\n")

        
        
        elif user_choice == "4":                                                                                #Disconnect from server and close client program
            message = message = "SETSTATUS \r\n" + "USERNAME {}\r\n".format(username) +  "OFFLINE\r\n\r\n"
            clientSocket.send(message.encode())
            clientSocket.close()
            exit()



def recv_messages():
    global peer_username
    connected = False
    try:
        while True:
            data, _ = chatSocket.recvfrom(1024)
            data = data.decode()
            data = decrypt(data)
            if connected==False:                                                            #Once user receives first message, their status is set to "BUSY"
                connected=True
                global username
                message = "SETSTATUS \r\n" + "USERNAME {}\r\n".format(username) +  "BUSY\r\n\r\n"   
                clientSocket.send(message.encode())
                returnmessage = clientSocket.recv(1024).decode()
    
                
            if data == 'QUIT':                                                         #In order to leave a chat, user types "QUIT_CHAT" - here it is received from the peer
                                                                                            #Global variable set
                print("{} has left the chat. Press enter to continue...".format(peer_username))
                chatSocket.close()
                return
            
            print('\r{}: {}\n> '.format(peer_username,data), end='')
    except:
        return
    

def send_messages(peer_ip,peer_port):
    try:
        while True:
            msg = input('> ')
            encmsg = encrypt(msg)                                                           #Encrypt the message for sending
            chatSocket.sendto(encmsg.encode(),(peer_ip, peer_port))
            if msg == 'QUIT':                                                          #In order to leave a chat, user types "QUIT_CHAT" - here it is sent to the peer
                print("Disconnected from chat.\n")
                chatSocket.close()
                return    
    except:
        return


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

def chat(peer_username,username):
    message = "CHAT \r\nSTART\r\n{}\r\n{}\r\n\r\n".format(peer_username,username)           #Message to server requesting chat information
    clientSocket.send(message.encode())
    returnmessage = clientSocket.recv(1024).decode()                                          #Chat info - peer status + other info if peer is available  
    command = returnmessage[:returnmessage.find("\r")]

    if command == "BUSY":
        print("User is currently busy.\n")
    
    elif command == "OFFLINE":
        print("User is currently offline.\n")

    elif command == "DNE":
        print("User does not exist.\n")

    elif command =="AVAILABLE":
        print("User available. Initializing chat...\n\n(To quit a chat at any time, type QUIT and press enter.)\n")                                        #AVAILABLE\r\npeerIP\r\npeerPort\r\n\r\n
        returnmessage = returnmessage[returnmessage.find("\n")+1:]
        ip_address = returnmessage[:returnmessage.find("\r")]
        returnmessage = returnmessage[returnmessage.find("\n")+1:]
        sport = returnmessage[:returnmessage.find("\r")]   

        sport = int(sport)

        global chatting
        chatting=True
        chat_thread = Thread(target=chat_session, args=(ip_address,sport,),daemon=True)                     #Thread for chatting
        chat_thread.start()
        chat_thread.join()
        

        message = "SETSTATUS \r\n" + "USERNAME {}\r\n".format(username) +  "AVAILABLE\r\n\r\n"              #Set user status back to Available once they have finished chatting
        clientSocket.send(message.encode())
        returnmessage = clientSocket.recv(1024).decode()
        global chatSocket
        chatSocket = socket(AF_INET, SOCK_DGRAM)   
        chatSocket.bind((clientSocket.getsockname()[0],0))
        message = "SOCKET \r\n{}\r\n{}\r\n\r\n".format(username,chatSocket.getsockname()[1])
        clientSocket.send(message.encode())
        returnmessage = clientSocket.recv(1024).decode()
    
def encrypt(message):                                               #Encryption using Caeser cipher - key = length of username
    global username
    global bank
    key = len(username)
    encrypted = ""
    for x in message:
        position = bank.find(x)
        newposition = (position+key)%73
        encrypted += bank[newposition]
    return encrypted

def decrypt(message):                                               #Decrypting message using peer's username as key
    global bank
    global peer_username
    key = len(peer_username)
    decrypted = ""
    for x in message:
        position = bank.find(x)
        newposition = (position-key)%73
        decrypted += bank[newposition]
    return decrypted

        
            
            
if __name__ == "__main__":
    main()