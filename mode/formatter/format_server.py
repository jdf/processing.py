import socket
from struct import pack, unpack
import sys
import autopep8

PORT = 10011

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10011)
sock.bind(server_address)
sock.listen(1)
print >>sys.stderr, 'Format server up on %s port %s' % server_address
while True:
    connection, client_address = sock.accept()
    try:
        buf = ''
        while len(buf) < 4:
            buf += connection.recv(4 - len(buf))
        (size,) = unpack('>i', buf)
        if size == -1:
            print >>sys.stderr, 'Format server exiting.'
            sys.exit(0)
        src = ''
        while len(src) < size:
            src += connection.recv(4096)
        src = src.decode('utf-8')
        reformatted = autopep8.fix_code(src)
        encoded = reformatted.encode('utf-8')
        connection.sendall(pack('>i', len(encoded)))
        connection.sendall(encoded)
    finally:
        connection.close()
