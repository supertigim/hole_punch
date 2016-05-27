# Relay Server is needed when punch hole does not work properly. 
#
# This daemon should run on a server with public IP 
#
# default port      : 4653
# max packet size   : 263 (compatible with MAVLINK)
# keep_alive time   : 30 (seconds) 
import socket
import struct
import sys
import time

DEFAULT_PORT    = 4653
MAVLINK_LENGTH  = 263
KEEP_ALIVE      = 30

def main():
    port = DEFAULT_PORT
    try:
        port = int(sys.argv[1])
    except (IndexError, ValueError):
        pass

    sockfd = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    sockfd.bind( ("", port) )
    print "listening on *:%d (udp)" % port

    connections = []

    while True:
        newconn = True
        conn_num = len(connections)    

        data, addr = sockfd.recvfrom(MAVLINK_LENGTH)
        
        cur_time = time.time()
        offset = 0
        
        for i in range (0, conn_num):
            target, last_time = connections[i-offset]
            if addr == target:
                connections[i-offset] = addr, cur_time
                newconn = False
            else:
                if (cur_time - last_time) > KEEP_ALIVE:
                    del connections[i-offset]
                    offset += 1
                else:     
                    sockfd.sendto( data, target )

        if newconn:
            connections.append((addr,cur_time))    

if __name__ == "__main__":
    main()

# vim: expandtab shiftwidth=4 softtabstop=4 textwidth=79: