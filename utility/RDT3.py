from torch import reciprocal
from UDP import udp_connetion


class RDT:
    def __init__(self, type, port):
        '''
            type: "client" ou "server"
        '''
        self.udp_connection = udp_connetion(type=type, port=port)
        self.sequence_number = 0
        self.data_buffer = None
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

    def make_pkt(self, data, checksum, sequence_number):
        return {"data": data,  "checksum": checksum,  "sequence_number": sequence_number}

    def make_ack(self, ack, checksum):
        return {"ack": ack, "checksum": checksum}

    def is_corrupt(self, ):
        pass

    def recieve(self, ):
        pass

    def send(self, msg_string):
        # creates the pkt
        pkt_to_send = self.make_pkt(self.seq_num, msg_string)

        # increments the sequence number
        self.seq_num += 1

        while True:
            ### sends the packet ###
            self.udp_connection.send(pkt_to_send.encode())

            # clears the data buffer
            self.data_buffer = None

            # variable for listening for incoming data
            recieved_pkt = None

            ### loops until recieves data ###
            while recieved_pkt == None:
                recieved_pkt = self.udp_connection.recieve().decode()

            # sets byte_buffer to received data
            self.data_buffer = recieved_pkt

            ### checks for corruption ###
            # if data is not corrupted, check sequence numbers
            if(not self.is_corrupt(recieved_pkt)):

                ### check sequence numbers ###
                # check to make sure the response sequence number isn't behind
                if recieved_pkt["sequence_number"] < self.sequence_number:
                    # creates ack pkt
                    ack = self.make_ack(1,)
class RDTClient: 
    pass 
