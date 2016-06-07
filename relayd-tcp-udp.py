from socket import *
from select import select

DEFAULT_PORT    = 4653
MAVLINK_LENGTH  = 263

def run():
    host = ''
    backlog = 5
    sock_GCS = None
    addr_udp = None

    # create tcp socket
    tcp = socket(AF_INET, SOCK_STREAM)
    tcp.bind(('',DEFAULT_PORT))
    tcp.listen(backlog)

    # create udp socket
    udp = socket(AF_INET, SOCK_DGRAM)
    udp.bind(('',DEFAULT_PORT))

    input = [tcp,udp]

    while True:
        inputready,outputready,exceptready = select(input,[],[])

        for s in inputready:
            if s == tcp:
                sock_GCS, addr = s.accept()
                input.append(sock_GCS)
            elif s == udp:
                data, addr_udp = s.recvfrom(MAVLINK_LENGTH)
                if sock_GCS is not None and data is not None:
                    sock_GCS.send(data)
            else:
                data = sock_GCS.recv(MAVLINK_LENGTH)
                if addr_udp is not None and data is not None:
                    udp.sendto( data, target )
                #print "unknown socket:", s

if __name__ == '__main__':
    run()