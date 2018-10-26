import sys
import socketserver
import threading
from threading import Thread
import json

class TCPHandler(socketserver.StreamRequestHandler):

    def handle(self):
        
        self.data = self.rfile.readline().strip()
        if self.data == bytes("QFT_REQUEST", 'UTF-8'):
            self.wfile.write("QFT_SUCCESS".encode('utf-8'))
        else:
            self.wfile.write("QFT_ERROR".encode('utf-8'))

class UDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        
        data = self.request[0].strip()
        socket = self.request[1]
        
        print(":"  +str(data) + ":")
        
        if data != bytes("X", 'UTF-8'):
            if data == bytes("QFT_REQUEST", 'UTF-8'):
                socket.sendto("QFT_SUCCESS".encode('utf-8'), self.client_address)
            else:
                socket.sendto("QFT_ERROR".encode('utf-8'), self.client_address)

class Server():
    
    def start(address ,port, type = "tcp"):
        if type =="tcp":
             server = socketserver.TCPServer((address,port), TCPHandler)
        elif type == "udp":
             server = socketserver.UDPServer((address,port), UDPHandler)
        else:
            print("Invalid Type!")
            sys.exit()
            
       
        print ("Starting server at " + str(port))
        t = Thread(target=server.serve_forever)
        t.start()
        
        
      
        

json_cfg = json.loads(open("server.cfg").read())

print(json_cfg)

for server_info in json_cfg:
    current_server = Server
    current_server.start( server_info['address'] , server_info['port'] , server_info['type'])



        