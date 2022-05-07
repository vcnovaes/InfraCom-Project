from utility.RDT3 import RDTConnection
import os

port = 3001

def main():
    os.system(f"kill -9 $(lsof -t -i:{port})")
    os.system("clear")

    server_connection = RDTConnection("server", "0.0.0.0", port)
    while True:
        pkt, client_addr = server_connection.receive("0.0.0.0", 3000)



if __name__ == '__main__': 
    main()