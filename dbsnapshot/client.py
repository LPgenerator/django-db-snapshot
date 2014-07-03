# -*- encoding: utf-8 -*-

import socket
import json


class Client(object):
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def send(self, method, *args):
        self.sock.sendall('%s:%s;' % (method, ','.join(args)))

    def recv(self):
        data = ''
        while True:
            data += self.sock.recv(1024)
            if ';' in data or not data:
                break
        if data:
            return json.loads(data.rstrip(';'))

    def close(self):
        self.sock.close()
