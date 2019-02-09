import socket
import threading
import timeit
import time

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

        
    def send_msg(self, item, msg=''):
        dat = header.TEMPLATE.format(item)
        self.sock_sender.send(bytes(dat))
        
        if msg == '':
            msg = 'sent data'
        lib.log_prefix_template(self.name, msg, dat)

        #simulated delay
        time.sleep(header.SLEEP_SEND)
        
        
    def close(self):
        #only need to close client socket
        self.sock_sender.shutdown(socket.SHUT_RDWR)
        self.sock_sender.close()
        
        #self.sock_receiver.shutdown(socket.SHUT_RDWR)
        #self.sock_receiver.close()

        
        