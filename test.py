import sys
import socket
from select import select
import struct

def main():
    try:
        target = (sys.argv[1], int(sys.argv[2]))
    except (IndexError, ValueError):
        print >>sys.stderr, "usage: %s <host> <port> " % sys.argv[0]
        sys.exit(65)

    sockfd = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    sockfd.sendto( "hi", target )
    
    while True:
        rfds,_,_ = select( [0, sockfd], [], [] )
        if 0 in rfds:
            data = sys.stdin.readline()
            if not data:
                break
            sockfd.sendto( data, target )
        elif sockfd in rfds:
            data, addr = sockfd.recvfrom( 1024 )
            sys.stdout.write( data )

    sockfd.close()

if __name__ == "__main__":
    main()

# vim: expandtab shiftwidth=4 softtabstop=4 textwidth=79: