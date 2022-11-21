# Frank Lugola
import socket
from socket import SOCK_STREAM, AF_INET, SOCK_DGRAM
from time import sleep
from random import randint
import argparse

server = "127.0.0.1"

port = 13


# tcp
def main1():
    print("Client here")
    with socket.socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect((server, port))
        
        response = sock.recv(2048).decode()
        print(f"Daytime: {response}")
    print("Client is done")


# udp
def main2():
    print("Client here")
    with socket.socket(AF_INET, SOCK_DGRAM) as sock:
        while True:
            msg = "udp"
            sock.sendto(msg.encode(), (server, port))
            response, _ = sock.recvfrom(2048)
            
            break 
        print(f"Daytime: {response.decode()}")
    print("Client is done")

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Parse arguments")
    arg_parser.add_argument("c", type=str, help="pick a protocol")
    
    args = arg_parser.parse_args()
    if args.c == "tcp":
        main1()
    elif args.c == "udp":
        main2()



# sources were notes from tcp and udp and also args from traceroute