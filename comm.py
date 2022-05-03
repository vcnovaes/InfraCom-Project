from checksum import append_checksum, extract_checksum, verify_checksum

IP = '127.0.0.1'
SERVER_PORT = 5003 
CLIENT_PORT = 1201

def send(sock, data, ip, port):
    data = append_checksum(bytearray(data))
    sock.sendto(data, (ip, port))


def recv(sock):
    data, addr = sock.recvfrom(1024)
    (data, chksum) = extract_checksum(data)
    if not verify_checksum(data, chksum):
        sock.close()
        assert False, "checksum failed"

    print('received {} from {}'.format(data, addr))

    return (data, addr)
