import endnode
import header
import Queue
import timeit
import threading
import lib
import numpy as np

class Server(endnode.EndPoint):
    buf_recv = None
    def __init__(self, name, local_addr, local_port, dest_addr, dest_port):
        self.buf_recv = Queue.Queue()
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
                self.send_msg(nak, msg='resent (NAK)')            
            
            
    def push_data(self):
        #server push data to client in flows
        for i in range(header.Y):            
            #check receive buffer, if there is a NAK, send the package
            #lib.log_prefix(self.name, 'received nak, will send data later')
            #then, send a data package
            self.send_msg(i)
