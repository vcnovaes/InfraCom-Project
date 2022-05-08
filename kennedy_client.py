import os

serverName = '127.0.0.1'
serverPort = 1200
clientSocket = socket(AF_INET, SOCK_DGRAM)

os.system(f"kill -9 $(lsof -t -i:{port})")
os.system("clear")


def enviar(msg):
    clientSocket.sendto(msg.encode(), (serverName, serverPort))

def receber():
    messageReceived, serverAddress = clientSocket.recvfrom(2048)
    messageReceived = messageReceived.decode()
    return messageReceived
while True:
    msg = input('Escreva algo: ')
    enviar(msg)
    msg = receber()
    if msg == 'Volte sempre':
        break
clientSocket.close()