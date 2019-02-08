import endnode
import header
import headerdll
import lib
import timeit

import numpy as np

class Client(endnode.EndPoint):
    buf_recv = None
    
    def __init__(self, name, local_addr, local_port, dest_addr, dest_port):
        self.buf_recv = [header.WINDOW_NODATA for i in range(headerdll.Y)]
        super(Client, self).__init__(name, local_addr, local_port, dest_addr, dest_port)
    
    def can_escape(self):
        if sum(self.buf_recv) == headerdll.Y:
            return True
        else:
            return False
        
    def check_and_close(self):
        if self.can_escape() == True:
            self.send_msg(header.PACKET_CLOSE)
            self.close()
        
    def check_nak(self):
        #TODO: return list of sequence number to be send nak
        result = []
        p = lib.last_occurence(self.buf_recv, header.WINDOW_HASDATA)
        if p == -1:
            return result
        for idx, item in enumerate(self.buf_recv[:p]):
            if item == header.WINDOW_NODATA:
                result.append(idx)
        return result
    
    def send_nak(self, nak_list):
        #np.random.shuffle(nak_list)
        #for item in nak_list[:header.CLIENT_NAKCOUNT]:
        for item in nak_list:#send all nak
            self.send_msg(item, msg='sent NAK')
            
    def handle_timeout(self):
        p = lib.last_occurence(self.buf_recv, header.WINDOW_HASDATA)
        self.send_nak([p+1])
    
    def accept(self):
        connection, address = self.sock_receiver.accept()
        while True:
            connection.settimeout(5.0)
            try:
                buf = connection.recv(header.PACKET_SIZE)
            except:
                #handling timeout
                self.handle_timeout()
                continue

                
            if buf != '':
                dat = int(buf)
                self.buf_recv[dat] = header.WINDOW_HASDATA
                lib.log_prefix_template(self.name,'received data',buf)            
                
                nak_list = self.check_nak()
                self.send_nak(nak_list)
                
                self.check_and_close()

            else:
                lib.log_prefix(self.name,'closing server...')
                break