import socket as skt
from time import time

class Server:
    def __init__(self, address, port, buffer_size, timeout) -> None:
        self.timeout = timeout
        self.sender_adress = address
        self.buffer_size = buffer_size
        #socket configurations
        self.UDP_socket = skt.socket(family=skt.AF_INET, type=skt.SOCK_DGRAM)
        self.UDP_socket.bind((address,port))
        self.UDP_socket.settimeout(timeout)
        print("Starting server")
        self.run() 
    
    def run(self):
        while(True):
            msg, sender_adress = self.receive_data() 


    def receive_data(self):
        print("Receiving data")
        msg, sender_address = self.UDP_socket.recvfrom(self.buffer_size)
        return self.rcv_pkt(data, sender_address), sender_address

    
    def rcv_pkt(self,data, sender_adress):
        data = data.decode() 
        sequence_num = data


class RDTClient: 
    pass 