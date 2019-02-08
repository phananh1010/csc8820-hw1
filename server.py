import Queue
import timeit
import threading
import numpy as np

import endnode
import header
import statistic
import lib

class Server(endnode.EndPoint):
    buf_recv = None
    stats = None
    def __init__(self, name, local_addr, local_port, dest_addr, dest_port):
        self.buf_recv = Queue.Queue()
        self.stats = statistic.Stats()
        t2 = threading.Thread(target=self.resend_nak)
        t2.start()
        super(Server, self).__init__(name, local_addr, local_port, dest_addr, dest_port)
        
    def accept(self):
        connection, address = self.sock_receiver.accept()
        while True:
            #lib.log_prefix(self.name, 'accepting data')
            buf = connection.recv(header.PACKET_SIZE)
            if buf != '':
                dat = int(buf)
                self.buf_recv.put(dat)
                if dat == header.PACKET_CLOSE:
                    #close connection, since the client got all the data
                    self.close()
                    break
                else:
                    lib.log_prefix_template(self.name,'received NAK', dat)   
            else:
                lib.log_prefix(self.name,'closing server...')
                break
                
    def resend_nak(self):
        print 'Starting resend nak thread'
        while True:
            nak = self.buf_recv.get()
            if nak == header.PACKET_CLOSE:
                break
            else:
                self.stats.log(self.stats.TRY)
                self.send_msg(nak, msg='resent (NAK)')            
            
            
    def push_data(self):
        #server push data to client in flows
        for i in range(header.Y):            
            #check receive buffer, if there is a NAK, send the package
            #lib.log_prefix(self.name, 'received nak, will send data later')
            #then, send a data package
            self.stats.log(self.stats.TRY)
            self.send_msg(i)
