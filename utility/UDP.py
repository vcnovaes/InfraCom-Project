from logging import exception
import socket


class udp_connetion:
    def __init__(self, type, port):
        '''
            type: "client" ou "server"
        '''

        if(type == "server"):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind(("localhost", port))
            print(f"UDP Server is listening on port {port}")

        elif(type == "client"):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        else:
            raise Exception(
                f"{type} is not a valid type. Must be either 'client' or 'server'.")

    def recieve(self):
        data, adress = self.socket.recvfrom(2048)
        return (data, adress)

    def send(self, data, reciever_ip):
        '''
            data must be in bytes (encoded)
        '''
        self.socket.sendto(data, ("localhost", reciever_ip))
        if(type == "client"):
            print(
                f"Client: {data.decode()} ({data})")
        elif(type == "server"):
            print(
                f"Server: {data.decode()} ({data})")

    def close(self):
        self.socket.close()
        print("Client closed")
