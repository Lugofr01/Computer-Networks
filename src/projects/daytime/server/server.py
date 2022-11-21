import socket
import time
host = "127.0.0.1"
port = 13

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 13)) 
server.listen(5)

while True:
    sock, addr = server.accept()
    daytime = time.strftime("%A, %B %d, %Y, %H:%M:%S-%Z\n") # Tuesday, February 22, 1982 17:37:43
    sock.send(daytime.encode("ascii"))
    sock.close()