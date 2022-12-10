#!/usr/bin/env python3
"""
`nameserver` implementation

@author:Frank Lugola
@version:
"""

import argparse
import struct
import logging
from socket import AF_INET, SOCK_DGRAM, socket

HOST = "localhost"
PORT = 43053

DNS_TYPES = {1: "A", 2: "NS", 5: "CNAME", 12: "PTR", 15: "MX", 16: "TXT", 28: "AAAA"}

TTL_SEC = {
    "1s": 1,
    "1m": 60,
    "1h": 60 * 60,
    "1d": 60 * 60 * 24,
    "1w": 60 * 60 * 24 * 7,
    "1y": 60 * 60 * 24 * 365,
}


def val_to_n_bytes(value: int, n_bytes: int) -> tuple[int]:
    """
    Split a value into n bytes
    Return the result as a tuple of n integers
    """
# TODO: Implement this function
    ...
    i =tuple([value >> i*8 & 255 for i in range(n_bytes-1, -1, -1)])
    return i


def bytes_to_val(bytes_lst: list) -> int:
    """Merge n bytes into a value"""
# TODO: Implement this function
    ...
    mergedValue = 0
    byteLength =len(bytes_lst)
    for j, i in enumerate(range(byteLength,0,-1)):
        mergedValue += bytes_lst[i-1] << (8*j)
    return mergedValue


def get_left_n_bits(bytes_lst: list, n_bits: int) -> int:
    """
    Extract first (leftmost) n bits of a two-byte sequence
    Return the result as a decimal value
    """
# TODO: Implement this function
    ...
    for i in bytes_lst:
        result= bytes_to_val(bytes_lst) >> (16 - n_bits)
    return result



def get_right_n_bits(bytes_lst: list, n_bits: int) -> int:
    """
    Extract last (rightmost) n bits of a two-byte sequence
    Return the result as a decimal value
    """
    # TODO: Implement this function
    ...
    for i in bytes_lst:
        result =int(bin(bytes_to_val(bytes_lst))[18 - n_bits:20],2)
    return result


    


def read_zone_file(filename: str) -> tuple:
    """
    Read the zone file and build a dictionary
    Use domain names as keys and list(s) of records as values
    """

    # TODO: Implement this function
    ...
    dictionary = {}
    values = ""
    with open(filename) as file:
        lines = file.readlines()

        origin,time  = lines[0].split(" ")[1].replace("\n", "")[:-1],lines[1].split(" ")[1].replace("\n", "")

      
        for i in lines[2:-1]:
            array = i.split(" ")
            partions = [j for j in array if j != ""]
        

            if i[0] != " ":
                values = partions[0]
                part = partions[1:]
            else:
                part = partions
            lengthPart = len(part) - 1

            if lengthPart  >= 3:
                ttoLive = part[lengthPart - 3]
            else:
                ttoLive = time
            
            if values not in dictionary:
                dictionary[values] = [(ttoLive, part[lengthPart - 2], part[lengthPart-1], part[lengthPart])]

            else:    
                dictionary[values].append((ttoLive, part[lengthPart - 2], part[lengthPart - 1], part[lengthPart])) 
                
    return (origin, dictionary)


def parse_request(origin: str, msg_req: bytes) -> tuple:
    """
    Parse the request and return query parameters as a tuple.
    """
 # Extract the domain name from the message and decode it.
    domain_start = 12
    domain_length = msg_req[12]
    domain = msg_req[domain_start+1:domain_start+1+domain_length].decode()
    
    id = bytes_to_val(msg_req[0:2])


    pointer = 0
    while msg_req[domain_start:][pointer] > 0:
        pointer += msg_req[domain_start:][pointer] + 1
    

    select= bytes_to_val(msg_req[domain_start:][pointer+1:pointer+3])
    
    if origin != "cs430.luther.edu":
        raise ValueError("Unknown origin")
    if select not in DNS_TYPES:
        raise ValueError("Unknown query type")
    if bytes_to_val(msg_req[domain_start:][pointer+3:pointer+5]) !=1:
        raise ValueError("Unknown class")


    return tuple([id,domain, select, msg_req[domain_start:]])
 

def format_response(
    zone: dict, trans_id: int, qry_name: str, qry_type: int, qry: bytearray
) -> bytearray:
    """Format the response"""
    # TODO: Implement this function
    ...
    formatResponse = [i for i in zone[qry_name] \
    if i[2] == DNS_TYPES[qry_type]]
    
    response = struct.pack(">HHHHHH", trans_id, 33024, 1, len(formatResponse)\
, 0, 0)
    response += qry
    for i in formatResponse:
        response += bytes([192, 12])
        response = response+ struct.pack(">HH", qry_type, 1)
        
        cleanedTTLStr = val_to_n_bytes(TTL_SEC[i[0]], 4)
        # ttoLive = qry

        ttoLive = bytearray()
        for j in cleanedTTLStr:
            ttoLive += bytes([j])
        response += ttoLive


        if qry_type == 1:
            strLength = len(i[len(i) - 1].split("."))
            response += struct.pack(">h", strLength)
            addrArray = [bytes([int(j)]) for j in i[len(i) - 1].split(".")]
            for i in addrArray:
                response += i
            

        else:
            response += struct.pack(">H", 16)
            ans = i[len(i) - 1].split(":")
            for i in ans:
                ans = val_to_n_bytes(int(i, 16), 2)
                for i in ans:
                    response = response + bytes([i])      
    return response





def run(filename: str) -> None:
    """Main server loop"""
    origin, zone = read_zone_file(filename)
    with socket(AF_INET, SOCK_DGRAM) as server_sckt:
        server_sckt.bind((HOST, PORT))
        print("Listening on %s:%d" % (HOST, PORT))

        while True:
            try:
                (request_msg, client_addr) = server_sckt.recvfrom(2048)
            except KeyboardInterrupt:
                print("Quitting")
                break
            try:
                trans_id, domain, qry_type, qry = parse_request(origin, request_msg)
                msg_resp = format_response(zone, trans_id, domain, qry_type, qry)
                server_sckt.sendto(msg_resp, client_addr)
            except ValueError as v_err:
                print(f"Ignoring the request: {v_err}")
def main():
    """Main function"""
    arg_parser = argparse.ArgumentParser(description="Parse arguments")
    arg_parser.add_argument("zone_file", type=str, help="Zone file")
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

    run(args.zone_file)


if __name__ == "__main__":
    main()
