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
