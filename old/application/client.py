from http import client
from utility.RDT3 import RDTConnection


def main():
    client_connection = RDTConnection("client", "0.0.0.0, 3000)
    try: 
        while True: 
            msg = input("Message to send:")
            client_connection.send(msg.encode(),"0.0.0.0 3001)
            
    except KeyboardInterrupt:
        client_connection.close()        



if __name__ == "__main__":
    main() 