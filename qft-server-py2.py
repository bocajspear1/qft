import sys
import SocketServer
import json
from threading import Thread
import threading
import atexit
import time

thread_list = []

should_connect_list = {}

class TCPHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        
        data = self.rfile.readline().strip()
        
        address = self.server.server_address[0]
        port = self.server.server_address[1]
        
        if self.server.should_connect == False:
            print("WARNING - Recieved unexpected packet on " + address + ":" + str(port) )
        else:
            print("Expected packet on " + address + ":" + str(port))
        
        
        if data == "QFT_REQUEST".encode('utf-8'):
            self.wfile.write("QFT_SUCCESS".encode('utf-8'))
        else:
            self.wfile.write("QFT_ERROR".encode('utf-8'))

class UDPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        
        data = self.request[0].strip()
        socket = self.request[1]
        
        address = self.server.server_address[0]
        port = self.server.server_address[1]
        
        if self.server.should_connect == False:
            print("WARNING - Recieved unexcepted packet on " + address + ":" + str(port) )
        else:
            print("Expected packet on " + address + ":" + str(port))

        
        if data != "X".encode('utf-8'):
            if data == "QFT_REQUEST".encode('utf-8'):
                socket.sendto("QFT_SUCCESS".encode('utf-8'), self.client_address)
            else:
                socket.sendto("QFT_ERROR".encode('utf-8'), self.client_address)



class TCPServerThread(threading.Thread):
    def __init__(self, address ,port, should_connect):
        threading.Thread.__init__(self)
        self.data = {}
        self.data['address'] = address
        self.data['port'] = port
        self.data['should_connect'] = should_connect
        
    def run(self):
        try:
            server = SocketServer.TCPServer((self.data['address'],self.data['port']), TCPHandler)
            server.should_connect = self.data['should_connect']
            print "Starting TCP server at " + str(self.data['port']) + "\n"
            server.serve_forever()
        except Exception as e:
            print "!- Error at starting TCP thread " + self.data['address'] + ":" + str(self.data['port']) + ", Error: " + str(e)
            

class UDPServerThread(threading.Thread):
    def __init__(self, address ,port, should_connect):
        threading.Thread.__init__(self)
        self.data = {}
        self.data['address'] = address
        self.data['port'] = port
        self.data['should_connect'] = should_connect
        
    def run(self):
        try:
            server = SocketServer.UDPServer((self.data['address'],self.data['port']), UDPHandler)
            server.should_connect = self.data['should_connect']
            print "Starting UDP server at " + str(self.data['port']) + "\n"
            server.serve_forever()
        except Exception as e:
            print "!- Error at starting UDP thread " + self.data['address'] + ":" + str(self.data['port']) + ", Error: " + str(e)
            
        
class Server():
   
    def start(self, address ,port, type, should_connect):
        try:
            
           
            
            if type == "tcp":
                 #server = SocketServer.TCPServer((address,port), TCPHandler)
                 server = TCPServerThread(address, port, should_connect)

            elif type == "udp":
                 #server = SocketServer.UDPServer((address,port), UDPHandler)
                 server = UDPServerThread(address, port, should_connect)

            else:
                print "Invalid Type!"
                sys.exit()
            
            server.daemon = True
            server.start()
            
            #server.should_connect = should_connect
           
            #print "Starting server at " + str(port)
            
            
            #thread_list.append(server)
            
            #t = Thread(target=server.serve_forever)
            #t.start()
        except Exception as e:
            print "!- Error at starting " + address + ":" + str(port) + ", Error: " + str(e)
       

try:
    
    json_cfg = json.loads(open("server.cfg").read())
    
    print "\nqft-client.py v1.2\n\n"
    
    for server_info in json_cfg:
        current_server = Server()
        current_server.start(server_info['server_address'], server_info['port'], server_info['type'], server_info['should_connect'])
    
    while True:
       time.sleep(1)
    
except IOError as e:
    print("Config file, server.cfg, not found")
    sys.exit()
except ValueError as e:
    print("Error in config JSON")
    sys.exit()


