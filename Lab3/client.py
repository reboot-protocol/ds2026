import socket
s = socket.socket()         


port = 1234      
HOST = '127.0.0.1'         


s.connect((HOST, port)) 

while True:
    data = input("type the command ")
    data = data.strip()
    s.send(data.encode())
    if(data == "/ls"):

        info = s.recv(1024).decode()
        print(info)
    
