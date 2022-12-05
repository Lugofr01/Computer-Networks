#!/usr/bin/env python3
"""Python Web server implementation"""
<<<<<<< HEAD
from logging.config import dictConfig
=======
>>>>>>> b463ff3dcae9ca1bb433108d634e6159088a47de
from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime
from time import sleep
from random import randint
import argparse
import logging
from pathlib import Path


SRVR_ADDR = "127.0.0.2"  # Local client is going to be 127.0.0.1
SRVR_PORT = 43080  # Open http://127.0.0.2:43080 in a browser
SRVR_NAME = ""


def parse_request(data: bytes) -> dict:
<<<<<<< HEAD

    """Parse the incoming request"""
    ...
    
    requestDictionary = {}
    parsedRequest = data.decode()
    parsedRequestLine = parsedRequest.split("\r\n")
    requestList = ["Accept","Host", "version", "url", "User-Agent", "method"]
    
    for i in requestList:
        if requestList[0]:
            requestDictionary[requestList[0]] = parsedRequestLine[3].split(": ")[1].strip()   

        if requestList[1]:
            
            requestDictionary[requestList[1]] = parsedRequestLine[1].split()[1].strip()

        if requestList[2]:
            requestDictionary[requestList[2]] = parsedRequestLine[0].split()[2].strip()

        if requestList[3]:
            requestDictionary[requestList[3]] = parsedRequestLine[0].split()[1]

        if requestList[4]:
            requestDictionary[requestList[4]] = parsedRequestLine[2].split(": ")[1].strip()

        if requestList[5]:
            requestDictionary[requestList[5]] = parsedRequestLine[0].split()[0]

    return requestDictionary


=======
    """Parse the incoming request"""
    ...
>>>>>>> b463ff3dcae9ca1bb433108d634e6159088a47de


def format_response(
    http_version: str, status_code: int, header: dict = {}, data: str = ""
) -> bytes:
    """Format the response"""
    ...
<<<<<<< HEAD
    messagelist =["OK","Not Found","Method Not Allowed","Not Implemented"]
    length =len(data)
    

    if status_code == 200:
            
            if header:
                return (f"{http_version} {status_code} OK\r\nDate: {datetime.now()}\r\nServer: CS430/2022\r\nContent-Type: {header['Content-Type']}\r\nLast-Modified: {header['Last-Modified']}\r\nContent-Length: {length}\r\n\r\n{data}".encode())
                
            return (f"{http_version} {status_code} {messagelist[0]}\r\nDate: {datetime.now()}\r\nServer: CS430/2022\r\nContent-Length: {length}\r\n\r\n{data}".encode())
   
    # return (f"{http_version} {status_code} OK\r\nDate: {datetime.now()}\r\nServer: CS430/2022\r\nContent-Type: {header['Content-Type']}\r\nLast-Modified: {header['Last-Modified']}\r\nContent-Length: {length}\r\n\r\n{data}".encode())
#################################################################################################################################################################################################################################################

    if status_code == 404:
           
            if header:
                return (f"{http_version} {status_code} \
                OK\r\nDate: {datetime.now()}\r\nServer: CS430/2022\r\nContent-Type: {header['Content-Type']}\r\nLast-Modified: {header['Last-Modified']}\r\nContent-Length: {length}\r\n\r\n{data}".encode())
   
            return (f"{http_version} {status_code} {messagelist[1]}\r\nDate: {datetime.now()}\r\nServer: CS430/2022\r\nContent-Length: {length}\r\n\r\n{data}".encode())
#################################################################################################################################################################################################################################################
    if status_code == 405:
           
            if header:
                return (f"{http_version} {status_code} \
                OK\r\nDate: {datetime.now()}\r\nServer: CS430/2022\r\nContent-Type: {header['Content-Type']}\r\nLast-Modified: {header['Last-Modified']}\r\nContent-Length: {length}\r\n\r\n{data}".encode())
            
            return (f"{http_version} {status_code} {messagelist[2]}\r\nDate: {datetime.now()}\r\nServer: CS430/2022\r\nContent-Length: {length}\r\n\r\n{data}".encode())
    
#################################################################################################################################################################################################################################################
    if status_code == 501:
           
            if header:
                return (f"{http_version} {status_code} \
                OK\r\nDate: {datetime.now()}\r\nServer: CS430/2022\r\nContent-Type: {header['Content-Type']}\r\nLast-Modified: {header['Last-Modified']}\r\nContent-Length: {length}\r\n\r\n{data}".encode())
            else:
                if length == 0:
                    return (f"{http_version} {status_code} {messagelist[3]}\r\nDate: {datetime.now()}\r\nServer: CS430/2022\r\n\r\n".encode())
                
                return (f"{http_version} {status_code} {messagelist[3]}\r\nDate: {datetime.now()}\r\nServer: CS430/2022\r\nContent-Length: {length}\r\n\r\n{data}".encode())

=======
>>>>>>> b463ff3dcae9ca1bb433108d634e6159088a47de


def server_loop(logfilename: Path):
    """Main server loop"""
    print("The server has started")
    with socket(AF_INET, SOCK_STREAM) as sock:
        ...



def main():
    """Set up arguments and start the main server loop"""
    arg_parser = argparse.ArgumentParser(description="Parse arguments")
    arg_parser.add_argument("logfile", type=str, help="Log file name")
    arg_parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable logging.DEBUG mode"
    )
    args = arg_parser.parse_args()

    logger = logging.getLogger("root")
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logger.level)

    server_loop(Path(args.logfile))


if __name__ == "__main__":
    main()
