from socket import *
servername="127.0.0.1"
serverport=12000
clientSocket=socket(AF_INET,SOCK_DGRAM)
sentence=input("enter the file")
clientSocket.sendto(bytes(sentence,"utf-8"),(servername,serverport))
filecontents,serverAddress=clientSocket.recvfrom(2048)
print("from server : ",filecontents)
clientSocket.close()
