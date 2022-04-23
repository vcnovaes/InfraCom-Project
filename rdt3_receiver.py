from checksum import *

def corrupt_data(data, checkS):
    aux = Checksum(len(data), data, False)
    if checkS + aux == 0xFFFF:
        return True
    return False


def make_pkt(is_checksum_valid, seq_do_reciever): 
    return { "is_checksum_valid": is_checksum_valid, "sequence" : seq_do_reciever}


def has_seq0(rck_pkt):
    if rck_pkt["sequence"] == 0: 
        return True
    else:
        return False

def has_seq1(rcvpkt):
    if rcvpkt["sequence"] ==1: 
        return True
    else:
        return False
