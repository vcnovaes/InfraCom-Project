from socket import *
import checksum
import rdt3_sender
import rdt3_receiver
import datetime


serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
seq_sender = 0
seq_receiver = 0



def send_pkt(pkt):
    max_time = 10

    # acting as SENDER
    # envia o pkt, inicia timer e, a cada estouro de timer, re-envia o pkt e reinicia o timer. Ao receber o ACK do reciever, sai do while.
    recieved_correct_ack = False
    while(recieved_correct_ack == False):
        clientSocket.sendto(pkt.encode(), (serverName, serverPort))
        start_time = datetime.datetime.now()

        # enquanto o timer não estourar, checa se recebeu o ack. 
        # se receber a mensagem, sai do while e vai para o while de cima (onde ele envia o pkt de novo)
        while(datetime.datetime.now() - start_time < max_time and recieved_correct_ack == False ):
            recieved_pkt, serverAddress = clientSocket.recvfrom(2048)
            # checa se recebeu um ack e seta o valor da variável recieved_ack 

            # se recebeu ack da sequencia certa e o checksum calculado no reciever foi True, set recieved_correct_ack to True, o que vai fazer sair dos dois whiles. 
            if( rdt3_sender.isAck(recieved_pkt, seq) and recieved_pkt["is_checksum_valid"] == True ):
                recieved_correct_ack = True
                seq = (seq + 1)%2


def recieve_pkt():
    
    # while not recieved correct pkt, continua a tentar receber pkt e envia seq errado. Se recebeu correct pkt, envia ACK correto e sai do while. 
    recieved_corret_pkt = False
    recieved_pkt = None
    while(recieved_corret_pkt == False):
        recieved_pkt, serverAddress = clientSocket.recvfrom(2048)

        is_checksum_valid = rdt3_receiver.corrupt_data(recieved_pkt["data"],recieved_pkt["checksum"])
        is_seq_correct = recieved_pkt["seq"] == seq_receiver
        
        pkt_do_receiver = None

        if(is_checksum_valid and is_seq_correct):
            # monta o pkt com feedback com seq do receiver
            pkt_do_receiver = rdt3_receiver.make_pkt(is_checksum_valid, seq_receiver)
            # envia o pkt com feedback(ACK)
            clientSocket.sendto(pkt_do_receiver.encode(), (serverName, serverPort))
            seq_receiver = (seq_receiver+1)%2
            recieved_corret_pkt = True # seta a variável dizendo que recebeu correto --> sai do while
        else:
            #caso esteja corrompido ou sequência diferente, manda o pkt_do_receiver com seq diferente do receiver
            pkt_do_receiver = rdt3_receiver.make_pkt(is_checksum_valid, (seq_receiver+1)%2)
            # envia o pkt com feedback(ACK)
            clientSocket.sendto(pkt_do_receiver.encode(), (serverName, serverPort))
    #retorna o pacote recebido
    return recieved_pkt


while True:

    message = input('Input lowercase sentence: ')
    if message == 'close':
        break

    # manda string minúscula (o server vai enviar minúscula)
    # client envindo uma mensage para o server
    checkS = checksum.Checksum(1, message)
    pkt = rdt3_sender.make_pkt(message, checkS, seq_sender)
    send_pkt(pkt)
    
    # cliente recebendo uma mensagem do server (string minúscula)
    string_que_o_server_modificou = recieve_pkt()["data"]
    print(string_que_o_server_modificou.decode())

clientSocket.close()