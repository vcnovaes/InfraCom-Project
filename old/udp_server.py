import socket
from comm import recv, send, SERVER_PORT, CLIENT_PORT



#def send_pkt(pkt, clientAdress):
#    max_time = 10
#
#    # acting as SENDER
#    # envia o pkt, inicia timer e, a cada estouro de timer, re-envia o pkt e reinicia o timer. Ao receber o ACK do reciever, sai do while.
#    recieved_correct_ack = False
#    while(recieved_correct_ack == False):
#        serverSocket.sendto(pkt.encode(), clientAdress)
#        start_time = datetime.datetime.now()
#
#        # enquanto o timer não estourar, checa se recebeu o ack. 
#        # se receber a mensagem, sai do while e vai para o while de cima (onde ele envia o pkt de novo)
#        while(datetime.datetime.now() - start_time < max_time and recieved_correct_ack == False ):
#            recieved_pkt, clientAdress = serverSocket.recvfrom(2048)
#            # checa se recebeu um ack e seta o valor da variável recieved_ack 
#
#            # se recebeu ack da sequencia certa e o checksum calculado no reciever foi True, set recieved_correct_ack to True, o que vai fazer sair dos dois whiles. 
#            if( rdt3_sender.isAck(recieved_pkt, seq) and recieved_pkt["is_checksum_valid"] == True ):
#                recieved_correct_ack = True
#                seq = (seq + 1)%2
#
#
#def recieve_pkt():
#    
#    # while not recieved correct pkt, continua a tentar receber pkt e envia seq errado. Se recebeu correct pkt, envia ACK correto e sai do while. 
#    recieved_corret_pkt = False
#    recieved_pkt = None
#    while(recieved_corret_pkt == False):
#        recieved_pkt, clientAdress = serverSocket.recvfrom(2048)
#
#        is_checksum_valid = rdt3_receiver.corrupt_data(recieved_pkt["data"],recieved_pkt["checksum"])
#        is_seq_correct = recieved_pkt["seq"] == seq_receiver
#        
#        pkt_do_receiver = None
#
#        if(is_checksum_valid and is_seq_correct):
#            # monta o pkt com feedback com seq do receiver
#            pkt_do_receiver = rdt3_receiver.make_pkt(is_checksum_valid, seq_receiver)
#            # envia o pkt com feedback(ACK)
#            serverSocket.sendto(pkt_do_receiver.encode(), clientAdress)
#            seq_receiver = (seq_receiver+1)%2
#
#            recieved_corret_pkt = True # seta a variável dizendo que recebeu correto --> sai do while
#        else:
#            #caso esteja corrompido ou sequência diferente, manda o pkt_do_receiver com seq diferente do receiver
#            pkt_do_receiver = rdt3_receiver.make_pkt(is_checksum_valid, (seq_receiver+1)%2)
#            # envia o pkt com feedback(ACK)
#            serverSocket.sendto(pkt_do_receiver.encode(), clientAdress)
#    #retorna o pacote recebido
#
#    return [recieved_pkt, client_port]
#
#
#
#
#

port = SERVER_PORT
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', port))

while True:

    recv(sock)

    #reciever
    # recebe mensagem minúscula
    # recieved_pkt, clientAddress = serverSocket.recvfrom(2048)
    #recieved_pkt, client_port = recieve_pkt()
    #message = recieved_pkt["data"]
    #print("I'm recieving: ", message.decode())
    #
    #
    ## modifica a mensagem (deixa tudo maiúsculo)
    #modifiedMessage = message.decode().upper()

    ## gera um novo pkt para enviar
    #checkS = checksum.Checksum(1, modifiedMessage)
    #pkt_with_modified_message = rdt3_sender.make_pkt(modifiedMessage, checkS, seq_sender)

    ##sender
    ## envia a mensagem modificada
    ## serverSocket.sendto(modifiedMessage.encode(), clientAddress)
    #send_pkt(pkt_with_modified_message, client_port)
