#!/usr/bin/env python3

import sys
import socket as sock


def serve(HOST, PORT):
    with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            try:
                while True:
                    data = conn.recv(1024)
                    #if not data:
                    #break
                    #conn.sendall(data)
            except KeyboardInterrupt:
                s.close()


def main(argv):
    HOST = '127.0.0.1'
    PORT = 631
    serve(HOST, PORT)


if __name__ == '__main__':
    main(sys.argv[1:])