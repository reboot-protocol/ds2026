
import socket     
import os        
import time
print("Instructions: \n" 
"1, /ls: list all available file in the server filesystem \n " 
"2, /upload filename.extension : upload a file to the server filesystem \n " 
"3, /download filename.exetension : download file from the server filesystem \n")
print("use ctrl+c to turn exit")
s = socket.socket()         


port = 1234      
HOST = '127.0.0.1'         


s.connect((HOST, port)) 

while True:
    x = input("type the command:  ")
    temp = x.strip().split()
    if(x == "/ls"):
        s.send(x.encode())
        info = s.recv(1024).decode().strip()
        print(info)
    if(temp[0] == "/download"):
        filename = temp[1]
        s.send(x.strip().encode())
        res = s.recv(1024).decode().strip()
        filesize = res
        with open(filename,"wb") as file:
            data = s.recv(int(filesize))
            file.write(data)
    if (temp[0] == "/upload"):
        filename = temp[1]
        filesize = os.path.getsize(filename)
        info = "/upload" + " " + filename + " " + str(filesize)
        s.send(info.encode())
        with open(filename,"rb") as file:
            time.sleep(2)
            s.sendall(file.read())
            

