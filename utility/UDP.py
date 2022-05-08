import socket, time
from utility import checksum
import json, unidecode


def make_pkt(data: str, additional_pkt_parts):
    checker = checksum.calculate_checksum(data.encode())
    pkt_dict = {
        "data": data,
        "checksum": checker,
    }
    if additional_pkt_parts is not None:
        for part in additional_pkt_parts:
            pkt_dict[part["name"]] = part["value"]
    
    encoded_pkt = json.dumps(pkt_dict, indent=2).encode('utf-8')
    return encoded_pkt


class UDPConnetion:
    def __init__(self, type, adress, port, timeout=None):
        '''
            type: "client" ou "server"
        '''

        if(type == "server"):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind((adress, port))
            print(f"UDP Server is listening on port {port}")
            self.socket.settimeout(timeout)

        elif(type == "client"):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind((adress, port))
            self.socket.settimeout(timeout)

        else:
            raise Exception(
                f"{type} is not a valid type. Must be either 'client' or 'server'.")

    def receive(self):
        pkt, adress = self.socket.recvfrom(2048)
        return (pkt, adress)

    def send(self, data:str, receiver_address, receiver_port, additional_pkt_parts = None):
        '''
            data must be a string

            additional_pkt_parts: [{"name": "sequence_number", "value": sequence_number}, {...}, ...]
        '''

        # print(f"\n dentro do udp send ====> {data} <==== \n")
        # print(".....")
        # time.sleep(4)
        # print("__...")
        # time.sleep(4)
        # print("_____")

        data = unidecode.unidecode(data)

        pkt_to_send = make_pkt(data, additional_pkt_parts)
        self.socket.sendto(pkt_to_send, (receiver_address, receiver_port))

        if(type == "client"):
            print(
                f"Client: {data.decode()} ({data})")
        elif(type == "server"):
            print(
                f"Server: {data.decode()} ({data})")

    def close(self):
        self.socket.close()
        print("Client closed")
