from socket import *
ServerName = "127.0.0.1"
Serverport= 12000
serverSocket= socket(AF_INET,SOCK_STREAM)
serverSocket.bind((ServerName,Serverport))
serverSocket.listen(1)
print("the server is ready to use")
while 1:
    connectionSocket,addr = serverSocket.accept()
    sentence =connectionSocket.recv(1024).decode()
    file= open(sentence,"r")
    l=file.read(1024)
    connectionSocket.send(l.encode())
    file.close()
    connectionSocket.close()
