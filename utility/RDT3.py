import socket as socket
import utility.UDP as UDP
from utility.checksum import verify_checksum
import ast, time



def make_ack_pkt(sequence_number):
    return UDP.make_pkt(data="ACK", additional_pkt_parts= [{"name":"sequence_number", "value":sequence_number}])

def next_sequence_number(sequence_number):
    return 1 - sequence_number
    
def is_ACK_correct(pkt, expected_seq) -> bool:
    pkt = ast.literal_eval(pkt.decode())
    return (pkt["data"] == "ACK") and (pkt["sequence_number"] == expected_seq)


class RDTConnection:
    def __init__(self, type, address, port, buffer_size=2048, timeout=10) -> None:
        '''
            type: "server" ou "client"
        '''

        # config
        self.timeout = timeout
        self.sender_adress = address
        self.buffer_size = buffer_size
        self.udp_connection = UDP.UDPConnetion(type, address, port)
        self.sequence_number = 0


    def is_corrupt(self, received_pkt):
        # received_pkt is a dict turned into a string, encoded into bytes. So we do the reverse here:
        received_pkt_decoded = ast.literal_eval(received_pkt.decode())
        received_checksum = received_pkt_decoded["checksum"]

        received_data = received_pkt_decoded["data"]
        encoded_data = received_data.encode()
        return not verify_checksum(received_data.encode(), received_checksum) 
        

    def is_sequence_number_ok(self, received_pkt):
        # received_pkt is a dict turned into a string, encoded into bytes. So we do the reverse here:
        received_pkt_decoded = ast.literal_eval(received_pkt.decode())
        received_sequence_number = received_pkt_decoded["sequence_number"]
        return received_sequence_number == self.sequence_number

    def receive(self, sender_address, sender_port):
        #   variable for listening for incoming data
        received_pkt = None
        ### loops until receives data ###
        while received_pkt == None:
            (received_pkt, address) = self.udp_connection.receive()

            ### checks if data is corruped && if sequence ###
            if not self.is_corrupt(received_pkt) and self.is_sequence_number_ok(received_pkt):
                ### if everything is ok, sends an ACK ###
                self.udp_connection.send(data="ACK", receiver_address=sender_address, receiver_port=sender_port, additional_pkt_parts=[{"name":"sequence_number", "value":self.sequence_number}])

                ### flips sequence number ###
                self.sequence_number = next_sequence_number(self.sequence_number)

            else:
                ### if data is corrupted or sequence number is incorrect, sends an ACK ###
                self.udp_connection.send(data="ACK", receiver_address=sender_address, receiver_port=sender_port, additional_pkt_parts=[{"name":"sequence_number", "value":next_sequence_number(self.sequence_number)}])

        pkt_decoded = ast.literal_eval(received_pkt.decode())
        data_decoded = pkt_decoded["data"] 
        sequence_number_decoded = pkt_decoded["sequence_number"] 
        if data_decoded != "ACK": 
            print(f"Received message: {data_decoded}")
            # print(f"sequence_number: {self.sequence_number}")
            # print(f"sequence_number_received: {sequence_number_decoded}")
        return (received_pkt, address)

    def send(self, data, receiver_address, receiver_port) -> None:
        '''
            data must be in bytes
        '''

        self.udp_connection.send(data, receiver_address, receiver_port, additional_pkt_parts=[{"name":"sequence_number", "value": self.sequence_number}])
        ### waits for correct, non-corrupted ACK while re-sending the pakt_to_send at every timeout ###
        received_pkt = None
        try:
            # @TODO: fix this later
            self.udp_connection.socket.settimeout(None)
            (received_pkt, _) = self.receive(receiver_address, receiver_port )
            while not is_ACK_correct(received_pkt, self.sequence_number):
                (received_pkt, _) = self.receive(receiver_address, receiver_port )
        except socket.timeout as e:
             # Try again
             print(f'Socket timed out {e}')
             self.send(data, receiver_address, receiver_port)
             
        self.sequence_number = next_sequence_number(self.sequence_number)
        
    def close(self):
        self.udp_connection.close()
        print(f"{type} closed.")
