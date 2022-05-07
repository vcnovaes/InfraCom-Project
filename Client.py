from http import client
from utility.UDP import UDPProtocol


def main():
    client_connection = UDPProtocol("localhost", 8080)

    while(True):
        try:
            msg = input("Send a message") 
            client_connection.rdt_send(msg.encode())  
            msg, adrr = client_connection.rdt_rcv() 
            print(msg, adrr)
        except KeyboardInterrupt as stop:
            client_connection.close() 





if __name__ == "__main__":
    main() 