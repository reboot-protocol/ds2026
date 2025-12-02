from mpi4py import MPI
import os
import socket
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
def serverfunc():
    current_dr = os.getcwd()
    os.chdir(current_dr+"/server")
    while True:
        command = comm.recv(source=1)
        if command == "/ls": 
             ls = str(os.listdir('.'))
             comm.send(ls,dest=1)
        if command.startswith("/download"):
            temp = command.split()
            filename = temp[1]
            with open(filename,"rb") as file:
                data = file.read()
                comm.send(data,dest=1)
        if command.startswith("/upload"):
            temp = command.split()
            filename = temp[1]
            respcode = 1
            comm.send(respcode,dest=1)
            with open(filename,"wb") as file:
                data = comm.recv(source=1)
                file.write(data)
    return 
def clientfunc():
        current_dr = os.getcwd()
        os.chdir(current_dr+"/client")
        
        s= socket.socket()
        port = 1234       
        HOST = '127.0.0.1'         
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, port))         
        s.listen(1)
        c, addr = s.accept()
        
        while True:
        
            x = c.recv(1024).decode().strip()
            temp = x.strip().split()
            if(x.strip() == "/ls"):
                command = x.strip()
                comm.send(command,dest=0)
                data=comm.recv(source=0)
                c.send(data.encode())
            if(x.startswith("/download")):
                filename = temp[1]
                command = x.strip()
                comm.send(command,dest=0)
                with open(filename,"wb") as file:
                     data = comm.recv()
                     file.write(data)
            if(x.startswith("/upload")):
                filename = temp[1]
                command = x.strip()
                comm.send(command,dest=0)
                respond = comm.recv(source=0)
                print(respond)
                if (respond == 1):
                    with open(filename,"rb") as file:
                        data = file.read()
                        comm.send(data,dest=0)
            


if rank == 0:
    serverfunc()
elif rank == 1:
    clientfunc()