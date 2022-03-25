from socket import socket, AF_INET, SOCK_DGRAM

def send_message(message, server):
    print("Sending message to target...")
    print(f"Target:  IP={server.ip} , PORT={server.port}")
    skt = socket(AF_INET,SOCK_DGRAM)
    skt.sendto(message, (server.ip, server.port))    



UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = b"Hello, World!"

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE)

sock = socket(AF_INET, # Internet
                     SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))