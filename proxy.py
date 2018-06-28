import socket
import os
import importlib
from threading import Thread

import parser

import sys
livereload = (len(sys.argv) <= 1)

class Proxy2Server(Thread):
    def __init__(self, host, port):
        super(Proxy2Server, self).__init__()
        self.game = None # game client socket not known yet
        self.port = port
        self.host = host
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))

    # run in thread
    def run(self):
        while True:
            data = self.server.recv(4096)
            if data:
                data_preview = data[:10].hex()
                #print(f'p2s[{self.port}] <- {data_preview}')

                try:
                    if livereload: importlib.reload(parser)
                    data = parser.parse(data, self.port, 'server')
                except Exception as e:
                    print(f'p2s[{self.port}] error'.format(), e)

                # forward to client
                self.game.sendall(data)
            else:
                pass
                #print(f'p2s[{self.port}] error receiving data'.format())

class Game2Proxy(Thread):
    def __init__(self, host, port):
        super(Game2Proxy, self).__init__()
        self.server = None # real server socket not known yet
        self.port = port
        self.host = host
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)
        # waiting for a connection
        print(f'g2p[{self.port}] waiting for a connection')
        self.game, addr = sock.accept()
        print(f'g2p[{self.port}] someone connected')

    def run(self):
        while True:
            data = self.game.recv(4096)
            if data:
                data_preview = data[:10].hex()
                #print(f'g2p[{self.port}] -> {data_preview}')

                try:
                    if livereload: importlib.reload(parser)
                    data = parser.parse(data, self.port, 'client')
                except Exception as e:
                    print(f'g2p[{self.port}] error', e)

                # forward to server
                self.server.sendall(data)
            else:
                pass
                #print(f'g2p[{self.port}] error receiving data'.format())


class Proxy(Thread):
    def __init__(self, from_host, from_port, to_host, to_port):
        super(Proxy, self).__init__()
        self.from_host = from_host
        self.from_port = from_port
        self.to_host = to_host
        self.to_port = to_port

    def run(self):
        while True:
            print(f'[helper class[{self.from_host}, {self.from_port}, {self.to_host}, {self.to_port}] setting up...')

            self.g2p = Game2Proxy  (self.from_host, self.from_port) # waiting for a client
            self.p2s = Proxy2Server(self.to_host,   self.to_port)

            self.g2p.server = self.p2s.server
            self.p2s.game   = self.g2p.game

            print(f'[helper class[{self.from_host}, {self.from_port}, {self.to_host}, {self.to_port}] All set up. Calling start()...')

            self.g2p.start()
            self.p2s.start()

            print(f'[helper class[{self.from_host}, {self.from_port}, {self.to_host}, {self.to_port}] Called start. Bye!')


master_server = Proxy('0.0.0.0', 4000, '127.0.0.1', 25565)
master_server.start()

while True:
    try:
        cmd = input('')
        if cmd[:4] == 'quit':
            os._exit(0)
        if cmd[:1] == 'r':
            importlib.reload(parser)        
    except Exception as e:
        print('MAIN THREAD', e)


