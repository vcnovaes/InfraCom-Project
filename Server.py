


from utility.UDP import UDPProtocol

def main():
    server = UDPProtocol(
        'localhost', 8080, is_server=True
    ) 
    while True:
        rcv_pkt, client_addr = server.rdt_rcv()
        pkt = eval(rcv_pkt.decode())
        print(f'Connected with: { client_addr}' )
        print(pkt.values())

        server.rdt_send(str(client_addr[1]).encode(), client_addr)


if __name__ == '__main__': 
    main()