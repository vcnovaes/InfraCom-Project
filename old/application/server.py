from utility.RDT3 import RDTConnection

def main():
    server_connection = RDTConnection("server", "locahost", 3001)
    
    state = 0 
    while True:
        if state == 1:      
            pkt, client_addr = server_connection.receive("localhost", 3000)
            msg = "Digite sua mesa"
            server_connection.send(msg,client_addr, )

if __name__ == '__main__': 
    main()