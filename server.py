import endnode
import header
import Queue
import timeit
import lib
import numpy as np

class Server(endnode.EndPoint):
    buf_recv = None
    def __init__(self, name, local_addr, local_port, dest_addr, dest_port):
        self.buf_recv = Queue.Queue()
        super(Server, self).__init__(name, local_addr, local_port, dest_addr, dest_port)
        
    def accept(self):
        connection, address = self.sock_receiver.accept()
        while True:
            #lib.log_prefix(self.name, 'accepting data')
            buf = connection.recv(header.PACKET_SIZE)
            if buf != '':
                dat = int(buf)
                self.buf_recv.put(dat)
                lib.log_prefix(self.name,'received data {}'.format(dat) )   
            else:
                lib.log_prefix(self.name,'received empty data')
                break
            
    def push_data(self):
        #server push data to client in flows
        for i in range(header.Y):
            
            if i == 2 and np.random.rand() > 0.3:
                lib.log_prefix(self.name, 'DROP packet')
                continue
            
            #check receive buffer, if there is a NAK, send the package
            if self.buf_recv.empty() == False:
                nak = self.buf_recv.get()
                self.send_msg(nak, msg='resent (NAK)')
                #lib.log_prefix(self.name, 'received nak, will send data later')
            #then, send a data package
            self.send_msg(i)
