from socket import *
import sys, subprocess
from threading import Thread


# serverName = "192.168.56.1"
serverName = "localhost"
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
# udp ports
chatSocket = socket(AF_INET, SOCK_DGRAM)
chatSocket.bind((clientSocket.getsockname()[0],0))

# def listen():
    
#     while True:
#         request, sender = chatSocket.recvfrom(1024)
#         request = request.decode()

#         if (request[0:request.find("\r")] == 'CHAT REQUEST '):
#             response = input("Someone requested to chat to you. Accept? (y/n): ")
#             peer_name = request[request.find("\n") + 1 : request.find("=")]
#             peer_ip = request[request.find("=") + 1 : request.find(":")]
#             peer_port = int(request[request.find(":") + 1:])
#             if response =='y':
#                 chatSocket.sendto("CHAT ACCEPTED".encode(), (peer_ip,peer_port))
#                 chat_session((peer_ip,peer_port),peer_name)
#                 return
#             else:
#                 chatSocket.sendto(f"CHAT REJECTED".encode(),(peer_ip,peer_port))
#                 return
                

def chat_session(peer_addr,peer_name):
    global exit_flag

    try:
        
        recv_thread = Thread(target=recv_messages,args=(peer_name, ))
        recv_thread.start()

        send_messages(peer_addr)

        recv_thread.join()
        exit_flag = False
        return
    
    except:
        print("Peer Disconnected")
        recv_thread.join()
        return
        

def recv_messages(peer_name):

    global exit_flag

    try:
        while not exit_flag:
            data, _ = chatSocket.recvfrom(1024)
            data = data.decode()
            if data == 'QUIT_CHAT':
                print("Peer left the chat")
                exit_flag = True
                return

            elif data == 'CHAT REJECTED':
                print("Chat request denied")
                exit_flag = True
                return

            print('\r{}: {}\n> '.format(peer_name, data), end='')

        return
    except:
        return


def send_messages(peer_addr):
    global exit_flag

    try:
        while not exit_flag:
            msg = input('> ')
            chatSocket.sendto(msg.encode(),(peer_addr[0], peer_addr[1]))
            if msg == 'QUIT_CHAT':
                exit_flag = True
                
                
        return
    except:
        return


def main():
    logged_in = False
    # listenerThread = Thread(target=listen, daemon=True)
    # listenerThread.start()
    
    while logged_in == False:
        username = input("Enter Username:\n")
        password = input("Enter Password:\n")
        message = "LOGIN " + "\r\n" + "USERNAME " + username + "\r\nPASSWORD " + password +"\r\nIP NUMBER "+clientSocket.getsockname()[0] + "\r\nUDP PORT " + str(chatSocket.getsockname()[1]) + "\r\n\r\n"
        
        print(message)
        clientSocket.send(message.encode())
        returnmessage = clientSocket.recv(1024).decode()
        #Decision Tree
        returncommand = returnmessage[:returnmessage.find("\r")-1]
        reason = returnmessage[returnmessage.find("\n")+1:-5]

        if returncommand == "UNSUCCESSFUL":
            if reason == "DUPLICATE":                                                       # If user logged in already
                print("User ({}) already logged into the server.".format(username))
                logged_in = True
            else:                                                                           # If incorrect password
                print("Password incorrect.")
            
        else:                                                                               # If successful - logged_in = True
            if reason == "NEW":
                print ("New user successfully registered.")
            else:
                print ("Welcome back {}!".format(username))
            
           
            logged_in = True


    while logged_in == True:

        message = "GETSTATUS \r\n" + "USERNAME " + username +"\r\n\r\n"
        clientSocket.send(message.encode())
        returnmessage = clientSocket.recv(1024).decode()
        print ("Your status is: " + returnmessage[returnmessage.find("\n")+1:]) #Protocol : "STATUS \r\n userstatus\r\n\r\n"
    
        options = "Choose an option:\n[1] Chat\n[2] List Clients\n[3] Set Status\n[4] Log Out\n"              #String of options to be displayed
 
        user_choice = (input(options))#add all options

        if user_choice == "1":                                  #Enter peer details and then connect with UDP
                
            peer_username = input("Enter Peer Username:\n")
            message = "CHAT \r\n" + "{}\r\n\r\n".format(peer_username)
            clientSocket.send(message.encode())  
            response = clientSocket.recv(1024).decode()
            
            if response == 'USER NOT FOUND':
                print("Invalid user")
                continue
            elif response == 'UNAVAILABLE':
                print("User is currently not available")
                continue

            print(response)

            peer_name = response[0: response.find("=")]
            peer_ip = response[response.find("=")+1:response.find(":")]
            peer_port = int(response[response.find(":") + 1:])
            
            global exit_flag
            exit_flag = False
            chat_thread = Thread(target=chat_session, args=((peer_ip,peer_port),peer_name),daemon=True)
            chat_thread.start()

            chat_thread.join()
            continue
           
            

        # elif user_choice == "5":                                           #Last option
        #     message = "SETSTATUS \r\n" + "USERNAME {}\r\n".format(username) +  "OFFLINE\r\n\r\n"
        #     clientSocket.send(message.encode())
        #     clientSocket.close()
        #     logged_in = False
            
        elif user_choice == "3":
            newstatus = input("What would you like to set your status to?\n1.) Available\n2.) Away\n")
            if newstatus == "1":
                message = "SETSTATUS \r\n" + "USERNAME {}\r\n".format(username) +  "AVAILABLE\r\n\r\n"
                clientSocket.send(message.encode())
            elif newstatus == "2":
                message = "SETSTATUS \r\n" + "USERNAME {}\r\n".format(username) + "AWAY\r\n\r\n"
                clientSocket.send(message.encode())
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
        

        elif user_choice == "4":
            message = "SETSTATUS \r\n" + "USERNAME {}\r\n".format(username) +  "OFFLINE\r\n\r\n"
            clientSocket.send(message.encode())                                         
            clientSocket.close()
            logged_in = False
            print("You have been Logged Out.")
   
if __name__ == "__main__":
    main()


