import socket
import threading
import timeit

 


import header
import lib

#client receiver port 6666
#server receiver port 6789

class EndPoint(object):#including client and server
    
    dest_addr = ''
    dest_port = -1
    
    local_addr = ''
    local_port = -1
    
    sock_sender = None
    sock_receiver = None
    
    name = ''
    
    def __init__(self, name, local_addr, local_port, dest_addr, dest_port):
        self.name = name
        self.dest_addr = dest_addr
        self.dest_port = dest_port
        self.local_addr = local_addr
        self.local_port = local_port
        
        self.sock_receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_receiver.bind((self.local_addr, self.local_port))#'localhost', 6789
        self.sock_receiver.listen(1)
        
        self.sock_sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        t = threading.Thread(target=self.accept)
        t.start()
        
        
        
        
        
    def connect(self):
        self.sock_sender.connect((self.dest_addr, self.dest_port))#'localhost', 6788
        


        
    def send_msg(self, item):
        dat = header.TEMPLATE.format(item)
        self.sock_sender.send(bytes(dat))
        lib.log_prefix(self.name, 'sent data {} {}'.format(dat, timeit.default_timer()%10000))
        

        
        