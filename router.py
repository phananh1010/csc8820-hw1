import socket
import threading
import time
import numpy as np

import header
import lib


class Router(object):
    inf1_dest_addr = ''
    inf1_dest_port = -1
    inf1_local_addr = ''
    inf1_local_port = -1
    
    inf2_dest_addr = ''
    inf2_dest_port = -1
    inf2_local_addr = ''
    inf2_local_port = -1
    
    inf1_sock_receiver = None
    inf1_sock_sender = None
    inf2_sock_receiver = None
    inf2_sock_sender = None
        
    name = ''
    
    def __init__(self, name, inf1_data, inf2_data):
        self.name = name
        self.inf1_local_addr, self.inf1_local_port, self.inf1_dest_addr, self.inf1_dest_port = inf1_data
        self.inf2_local_addr, self.inf2_local_port, self.inf2_dest_addr, self.inf2_dest_port = inf2_data
        
        
        self.inf1_sock_receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.inf1_sock_receiver.bind((self.inf1_local_addr, self.inf1_local_port))
        self.inf1_sock_receiver.listen(1)
        
        self.inf1_sock_sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #
        #t.start()
        
        self.inf2_sock_receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.inf2_sock_receiver.bind((self.inf2_local_addr, self.inf2_local_port))
        self.inf2_sock_receiver.listen(1)
        
        self.inf2_sock_sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        t12 = threading.Thread(target=self.forward, args=['forward 1->2', self.inf1_sock_receiver, self.inf2_sock_sender])
        t21 = threading.Thread(target=self.forward, args=['forward 2->1', self.inf2_sock_receiver, self.inf1_sock_sender])
        
        t12.start()
        t21.start()
        
    def connect(self):
        self.inf1_sock_sender.connect((self.inf1_dest_addr, self.inf1_dest_port))
        self.inf2_sock_sender.connect((self.inf2_dest_addr, self.inf2_dest_port))
        
    def drop(self, drop_chance, dat):
        if dat == header.PACKET_CLOSE:
            return False
        elif np.random.rand() <= drop_chance:
            return True
        else:
            return False

    def forward(self, label, sock_receiver, sock_sender):
        lib.log_prefix(self.name, 'preparing ' + label)
        connection, address = sock_receiver.accept()
        while True:
            buf = connection.recv(header.PACKET_SIZE)
            
            if buf=='':
                lib.log_prefix(self.name,'closing server...')
                break
            
            dat = int(buf)
                
            #decide to drop data
            if self.drop(header.DROP_CHANCE, dat) == True:
                lib.log_prefix_template(self.name, label + ' DROP packet', dat)
                continue #this line drops the data
            
            
            dat = header.TEMPLATE.format(dat)
            sock_sender.send(bytes(dat))
            lib.log_prefix_template(self.name, label, dat)
            
            if dat == header.PACKET_CLOSE:
                self.close()
        

    def close(self):
        #only need to close client socket
        self.inf1_sock_sender.shutdown(socket.SHUT_RDWR)
        self.inf1_sock_sender.close()
        
        self.inf2_sock_sender.shutdown(socket.SHUT_RDWR)
        self.inf2_sock_sender.close()
        
        