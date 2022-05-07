from cgi import print_exception
import socket as skt
import utility.checksum as cks
from utility.checksum import verify_checksum 

class UDPProtocol:
    def __init__(self, ip, port, is_server=False, timeout=1) -> None:
        self.socket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
        self.server_info = {"ip": ip, "port" : port}
        self.timeout = 1 
        self.seqnum = 0 
        if is_server:
            self.socket.bind(tuple(self.server_info.values()))
        pass
    
    def make_pkt(self, data, seqnum):
        checker = cks.calculate_checksum(data)
        pkt = {
            "checksum" : checker, 
            "sequence" : seqnum, 
            "data" : data
        }
        return pkt 

    def send_data(self, data, address=None):
        if address is None:
            address = tuple(self.server_info.values())
        return self.socket.sendto(data['data'], address)

    def rdt_send(self, data, address=None):
        address = tuple(self.server_info.values()) if address is None else address
        self.socket.settimeout(self.timeout)
        pkt = self.make_pkt(data,self.seqnum)
        hasAck = False

        while not hasAck:
            self.send_data(pkt,address)
            try:
                msg, address = self.socket.recvfrom(8000)
            except (skt.timeout, skt.error) as error:
                print_exception(error)
            ack = self.rcv_pkt(data)
        self.socket.settimeout(0)

    def rdt_rcv(self):
        pkt , address = self.socket.recvfrom(8000)
        isCorrupt = self.rcv_pkt(pkt, 'Receiver')
        if not isCorrupt:
            self.send(self.make_pkt(b'ACK',self.seqnum), address)
            self.seqnum  += 1 
        else:
            self.send(self.make_pkt(b'ACK', self.seqnum - 1)) 
        return pkt, address 
    
    def close(self):
        print("Closing connection")
        self.socket.close() 
    
    def rcv_pkt(self, data, isSender=True):
        pkt = eval(data.decode())
        
        if verify_checksum(data=data, checksum=pkt["checksum"]):
            print("Checksum ERROR")
            return False 
        if isSender and self.seqnum != pkt['sequence']:
            print("Sequence Number ERROR")
            return False 
        if isSender: 
            self.seqnum += 1 
        return True 

    