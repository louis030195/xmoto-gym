"""
TCP/UDP proxy.
"""

import argparse
import signal
import logging
import select
import socket
import numpy as np
import struct
import threading

class proxy:
    def __init__(self, src, dst, info):
        self.src = src
        self.dst = dst
        self.info = info
        self.sockets = []
        self.proxy_thread = threading.Thread(target=self.start, args=())
        self.proxy_thread.start()

    def start(self):
        """Run a proxy.
        
        Arguments:
        src -- Source IP address and port string. I.e.: '127.0.0.1:8000'
        dst -- Destination IP address and port. I.e.: '127.0.0.1:8888'
        """
        lock = threading.Lock()
        LOCAL_DATA_HANDLER = lambda x:x
        REMOTE_DATA_HANDLER = lambda x:x

        BUFFER_SIZE = 2 ** 10  # 1024. Keep buffer size as power of 2.

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(ip_to_tuple(self.src))
        s.listen(1)

        s_src, _ = s.accept()

        s_dst = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_dst.connect(ip_to_tuple(self.dst)) 
        
        self.sockets.append(s_src)
        self.sockets.append(s_dst)
        
        while True:
            s_read, _, _ = select.select(self.sockets, [], [])
            
            for s in s_read:
                data = s.recv(BUFFER_SIZE)
                try:
                    with lock:
                        self.info = dict(map(reversed, struct.unpack('BfffffHHHBbbbbbbbbbbbb', data.split(b'\n')[-2][:-1])))
                except:
                    pass
                
                if s == s_src:
                    d = LOCAL_DATA_HANDLER(data)
                    s_dst.sendall(d)
                elif s == s_dst:
                    d = REMOTE_DATA_HANDLER(data)
                    s_src.sendall(d)
    # end-of-function tcp_proxy    

    def close(self):
        self.proxy_thread.join()
        for s in self.sockets:
            s.close()


def ip_to_tuple(ip):
    """Parse IP string and return (ip, port) tuple.
    
    Arguments:
    ip -- IP address:port string. I.e.: '127.0.0.1:8000'.
    """
    ip, port = ip.split(':')
    return (ip, int(port))
    # end-of-function ip_to_tuple