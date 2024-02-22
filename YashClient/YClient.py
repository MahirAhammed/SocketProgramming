from socket import *
logged_in = False





serverName = ""
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

while logged_in == False:
    username = raw_input("Enter Username:\n")
    password = raw_input("Enter Password:\n")
    message = "LOGIN " + username.upper() + " " + password.upper()



sentence = raw_input("Input lowercase sentence:")
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print ("From Server:", modifiedSentence.decode())
clientSocket.close()



