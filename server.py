import endnode
import header
import Queue
import timeit
import lib

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
            dat = int(buf)
            self.buf_recv.put(dat)
            lib.log_prefix(self.name,'received data {}-{}'.format(dat, timeit.default_timer()%10000))    
            
    def push_data(self):
        #server push data to client in flows
        for i in range(header.Y):
            #check receive buffer, if there is a NAK, send the package
            if self.buf_recv.empty() == False:
                nak = self.buf_recv.get()
                self.send_msg(nak)
            #then, send a data package
            self.send_msg(i)
