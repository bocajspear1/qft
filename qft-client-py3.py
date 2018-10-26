import socket
import threading
from time import sleep
from threading import Thread
import json
import sys

def display_test(address, port,text_result, test):
    if (text_result == "QFT_SUCCESS" and test == True) or (text_result != "QFT_SUCCESS" and test == False):
        # Test is correct
        
        print("PASSED: Test for " + str(address) + ":" + str(port) + " resulted in " + str(test))
        
    else:
        
        print("FAILED: Test for " + str(address) + ":" + str(port) + " resulted in " + str(test))
    
def TCPTest(address, port, test):
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        my_socket.connect((address, port))
        
        fileobj = my_socket.makefile("rw")
        
    
        fileobj.write('QFT_REQUEST\n')
        fileobj.flush()
        
        result = fileobj.readline().strip()
        display_test(address, port, result, test)
    except ConnectionRefusedError as e:
        #print(e)
        display_test(address, port, "FAILED", test)
  
    
    my_socket.close()
    
def UDPTest(address, port, test):
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        my_socket.settimeout(2)
        
        my_socket.sendto("QFT_REQUEST".encode('utf-8'), (address, port))
        
        # receive data from client (data, addr)
        d = my_socket.recvfrom(1024)
        reply = d[0]
        addr = d[1]
        
        result = d[0].decode('utf-8').strip()
       
        display_test(address, port, result, test)
    except socket.timeout as e:
        display_test(address, port, "FAILED", test)


try:
    
    json_cfg = json.loads(open("client.cfg").read())
    
    print("qft-client.py v1.0\n\nConfig loaded. Starting tests in 2 seconds...\n\n")
    
    sleep(2)
    
    while True:
        for item in json_cfg:
            if item["type"] == "tcp":
                t = Thread(target=TCPTest, args=( item["address"], item["port"], item["test_for"]))
            elif item["type"] == "udp":
                t = Thread(target=UDPTest, args=( item["address"], item["port"], item["test_for"]))
            else:
                print("Invalid Type!")
                
            
            t.start()
        
        sleep(5)
        print("\n=======================================================\n")
except FileNotFoundError as e:
    print("Config file, client.cfg, not found")
    sys.exit()
except ValueError as e:
    print("")
    sys.exit()
