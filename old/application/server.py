from utility.RD3 import RDTConnection

def main():
    server_connection = RDTConnection("server", "locahost", 3001)
    while True:
        pkt, client_addr = server_connection.receive("localhost", 3000)


if __name__ == '__main__': 
    main()