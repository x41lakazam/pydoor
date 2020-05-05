#!/usr/local/bin/python3

import socket

def conn_handler(conn, addr):
    print("[v] Connected to", addr)
    while True:
        data = conn.recv(1024)
        print("-->", data.decode('utf-8'))

        if not data:
            conn.close()
            break
        cmd = input("$")
        conn.send(cmd.encode('utf-8'))


HOST = "0.0.0.0"
PORT = 35843

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

print("[*] Listening on {}:{}".format(HOST, PORT))
s.listen(1)

conn, addr = s.accept()
conn_handler(conn, addr)




