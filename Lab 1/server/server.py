
import socket   
import os     
import time
   


s = socket.socket()         
print ("Socket successfully created")


port = 1234       
HOST = '127.0.0.1'         


s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, port))         
print ("socket binded to %s" %(port)) 


s.listen(5)     
print ("socket is listening")            



c, addr = s.accept()     
print ('Got connection from', addr )
while True:
  textmess = c.recv(1024).decode().strip()
  if (textmess == "/ls"):
     list = str(os.listdir('.'))
     c.send(list.encode())
  if (textmess.startswith("/download")):
     temp = textmess.split()
     filename = temp[1]
     getsize = os.path.getsize(filename)
     filesize = str(getsize)
     c.send(filesize.encode())
     time.sleep(2)
     with open(filename,"rb") as file:
           c.sendall(file.read())

  if(textmess.startswith("/upload")):
    info = textmess.split()  
    filename = info[1]
    filesize = info [2]
    with open(filename,"wb") as file:
        data = c.recv(int(filesize))
        file.write(data)

  