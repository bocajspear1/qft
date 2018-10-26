import sys
import socket
import json

client_rules = []
server_rules = []
rule_num = 0
    
def valid_protocol(protocol):
    if protocol == "tcp" or protocol == "udp":
        return True
    else:
        return False

def valid_port(port):
    if (isinstance( port, ( int, long ) ) or port.isdigit()) and int(port) > 0 and int(port) < 65535:
        return True
    else:
        return False

def valid_ip(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
        return True
    except socket.error:
        return False
        
def valid_bool(input):
    if input == "false" or input == "true" or input == False or input == True:
        return True
    else:
        return False

def write_file(type):
    
    if type != "client" and type != "server":
        print "Invalid save type"
        sys.exit()
    
    will_write = False
        
    while will_write == False:
        try:
            
            file_name = raw_input("Enter " + type + " file name: ").replace("/","").replace("\\","")
            
            file_stream = open(file_name, 'a+')
            
            file_content = file_stream.read()

            # Rules to add
            add_rules = []
            
            if type == "server":
                add_rules = server_rules
            elif type == "client":
                add_rules = client_rules
            
            # If file not blank
            if file_content.strip() != "":
                valid_input = False
                res = ""
                
                while valid_input == False:
                    
                    res = raw_input("File is not empty, do you want to append (yn)? ")
                    
                    if res == "y" or res == "n":
                        valid_input = True

                
                if res == "y":
                    json_obj = json.loads(file_content)
                    add_rules = json_obj + add_rules
                
                
            #tcp 192.168.1.1 80 false
            
            #print add_rules

            
            file_stream.close()
            
            json.dump(add_rules, open(file_name, 'w'), sort_keys=True, indent=4)
                
            print(type + " config written to " + file_name)
            
            will_write = True
        except OSError as e:
            print ("\nCould not read/write file\n")
        except IOError as e:
            print ("\nCould not read/write file\n")
        except ValueError as e:
            print ("\nCould not read JSON in file\n")

def print_rules(rule_list):
    print "\n"
    for rule in rule_list:
        print rule['type'] + " server at " + rule['server_address'] + ":" + str(rule['port']) + ", should pass = " + str(str(rule['should_connect']))
        #print rule
    

while True:
    input_string = raw_input("> ")
    
    input_list =  input_string.split(" ")
    
    if input_list[0] == "done":
        
        
        write_file("server")
        write_file("client")
        
        sys.exit()
    elif input_list[0] == "exit" or input_list[0] == "quit":
         sys.exit()
    elif input_list[0] == "list":
        
        LENGTH = 2
        
        if len(server_rules) <= LENGTH:
            print_rules(server_rules)
        else:
            extra = len(server_rules) % LENGTH
            runs = (len(server_rules) - extra) / LENGTH
            
            if extra > 0:
                runs += 1
            
            start = 0
            
            for i in range(runs):
                print_rules(server_rules[start:start + LENGTH])
                
            
                start += LENGTH
                if i != runs - 1:
                    raw_input("== Enter to list more ==")
                else:
                    print "End of list"
            
            
    elif input_list[0] == "rule" and len(input_list) != 5:
        print "Invalid rule ( rule <protocol> <ip_address> <port> <should_pass: true | false> )"
    elif input_list[0] == "rule" and len(input_list) == 5:
        
        if "\"" in input_list and rule_num == 0:
            print "No previous rules ( <protocol> <ip_address> <port> <should_pass: true | false> )"
        else:
        
            if input_list[1] == "\"":
                protocol = client_rules[rule_num - 1]['type']
            else:
                protocol = input_list[1]
            
            if  input_list[2] == "\"":
                ip_addr = client_rules[rule_num - 1]['remote_address']
            else:
                ip_addr = input_list[2]
                
            if input_list[3] == "\"":
                port = client_rules[rule_num - 1]['port']
            else:
                port = input_list[3]
            
            if input_list[4] == "\"":
                should_pass = client_rules[rule_num - 1]['test_for']
            else:
                should_pass = input_list[4]
            
            
            if not valid_protocol(protocol) :
                print "Invalid protocol"
            elif not valid_ip(ip_addr) :
                print "Invalid IP address"
            elif not valid_port(port)  :
                print "Invalid port"
            elif not valid_bool(should_pass)  :
                print "Invalid value for should_pass"
            else:
                if should_pass == "true" or should_pass == True:
                    bool_sp = True
                else:
                    bool_sp = False
                
                    
                new_server_rule = {"type" : protocol, "server_address": ip_addr, "port": int(port), "should_connect": bool_sp}
                #print new_server_rule
                new_client_rule = {"type" : protocol, "remote_address": ip_addr, "port": int(port), "test_for": bool_sp}
                #print new_client_rule
                
                client_rules.append(new_client_rule)
                server_rules.append(new_server_rule)
                
                print "Rule added"
                
                rule_num += 1
    else: 
        print "Invalid command " + input_list[0]
