from socket import *

PORT=12001
HOST = ''

server = socket(AF_INET,SOCK_STREAM)
server.bind((HOST,PORT))

server.listen(10)
print("Waiting for connection...")

while True:
    connectionSocket, addr = server.accept()
    print(f"Connected to {addr}")

    message = connectionSocket.recv(1024).decode()
    print(message)

    response = "connected successfully"
    connectionSocket.send(response.encode())

    connectionSocket.close()

     
    