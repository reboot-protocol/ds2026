from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client

import os



with SimpleXMLRPCServer(('localhost', 8000)) as server:
        def download(filename):
              with open(filename, "rb") as handle:
                    return xmlrpc.client.Binary(handle.read())
        server.register_function(download,'download')
        def upload(filename,info):
              """
              print(type(info))
              print(type(filename))
              print(type(info.data))
              """
              with open(filename, "wb") as handle:
                    handle.write(info.data)
              return "success"
        server.register_function(upload,'upload')
        def list():
              ls = str(os.listdir('.'))
              return ls
        server.register_function(list,'list')
        server.serve_forever()