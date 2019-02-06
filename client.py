import endnode
import header
import lib
import timeit

class Client(endnode.EndPoint):
    buf_recv = None
    
    def __init__(self, name, local_addr, local_port, dest_addr, dest_port):
        self.buf_recv = [1] + [-1 for i in range(1, header.Y + 1)]
        super(Client, self).__init__(name, local_addr, local_port, dest_addr, dest_port)
    
    def accept(self):
        connection, address = self.sock_receiver.accept()
        while True:
            #lib.log_prefix(self.name, 'accepting data')
            buf = connection.recv(header.PACKET_SIZE)
            dat = int(buf)
            self.buf_recv[dat] = 1
            lib.log_prefix(self.name,'received data {}-{}'.format(dat, timeit.default_timer()%10000))            
    
            if dat % 7 == 0:
                self.send_msg(dat)
            
        