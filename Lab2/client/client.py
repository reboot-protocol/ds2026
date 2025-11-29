import xmlrpc.client


s = xmlrpc.client.ServerProxy('http://localhost:8000')

while True:
    x = input("type the command:  ")
    temp = x.strip().split()
    if(x == "/ls"):
        info = s.list()
        
        print(info)
    if(x.startswith("/download")):
        filename = temp[1]
        with open(filename,"wb") as file:
            file.write(s.download(filename).data)
        print("success")
    if (x.startswith("/upload")):
        filename = temp[1]
        with open(filename,"rb") as file:
            data = file.read()
            print(s.upload(filename,data))
        


