import endnode
import header
import lib
import timeit

class Client(endnode.EndPoint):
    buf_recv = None
    
    def __init__(self, name, local_addr, local_port, dest_addr, dest_port):
        self.buf_recv = [header.WINDOW_NODATA for i in range(header.Y)]
        super(Client, self).__init__(name, local_addr, local_port, dest_addr, dest_port)
    
    def can_escape(self):
        if sum(self.buf_recv) == header.Y:
            return True
        else:
            return False
        
        
    def check_nak(self):
        #TODO: return list of sequence number to be send nak
        result = []
        p = lib.last_occurrence(self.buf_recv, header.WINDOW_HASDATA)
        if p == -1:
            return result
        for idx, item in enumerate(self.buf_recv[:p]):
            if item == header.WINDOW_NODATA:
                result.append(idx)
        return result
    
    def send_nak(self, nak_list):
        for item in nak_list:
            self.send_msg(item)
    
    def accept(self):
        connection, address = self.sock_receiver.accept()
        while True:
            buf = connection.recv(header.PACKET_SIZE)
            if buf != '':
                dat = int(buf)
                self.buf_recv[dat] = header.WINDOW_HASDATA
                lib.log_prefix(self.name,'received data {}-{}'.format(buf, timeit.default_timer()%10000))            
                
                nak_list = self.check_nak()
                self.send_nak(nak_list)
                
                if self.can_escape() == True:
                    self.close()
            else:
                lib.log_prefix(self.name,'received empty data {}'.format(timeit.default_timer()%10000))   
                break
        