from socket import *
serverport=12000
ServerSocket=socket(AF_INET,SOCK_DGRAM)
ServerSocket.bind(("127.0.0.1",serverport))
print("server is ready to receive")
while True:
    sentence,clientAddress=ServerSocket.recvfrom(2048)
    file=open(sentence,"r")
    l=file.read(2048)
    ServerSocket.sendto(bytes(l,"utf-8"),clientAddress)
    print("send to client")
    file.close()
