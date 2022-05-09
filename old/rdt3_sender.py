from utility.checksum import *
import datetime


def make_pkt(data, checkS, seq):
    return {"data": data,  "checksum": checkS,  "sequence": seq}


def isAck(rcvpkt, seq):
    if rcvpkt["sequence"] == seq:
        return True
    return False


# TODO
def rdt_send(data, sendFunction):
    """
    returns the start time of the timer
    """
    sndpkt = make_pkt_sender(0, data, checksum)
    udt_send(sndpkt)
    return start_timer()
