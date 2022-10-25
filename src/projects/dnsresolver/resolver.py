#!/usr/bin/env python3
"""
`dnsresolver` implementation

@authors:Frank Lugola
@version: 2022.10
"""

import argparse
import logging
from random import choice, randint
from socket import AF_INET, SOCK_DGRAM, socket

PORT = 53

DNS_TYPES = {"A": 1, "AAAA": 28, "CNAME": 5, "MX": 15, "NS": 2, "PTR": 12, "TXT": 16}

PUBLIC_DNS_SERVER = [
    "1.0.0.1",  # Cloudflare
    "1.1.1.1",  # Cloudflare
    "8.8.4.4",  # Google
    "8.8.8.8",  # Google
    "8.26.56.26",  # Comodo
    "8.20.247.20",  # Comodo
    "9.9.9.9",  # Quad9
    "64.6.64.6",  # Verisign
    "208.67.222.222",  # OpenDNS
    "208.67.220.220",  # OpenDNS
]


def val_to_2_bytes(value: int) -> tuple[int]:
    """
    Split a value into 2 bytes
    Return the result as a tuple of 2 integers
    """
    # TODO: Implement this function
    ...
    val = (value >> 8 & 255, value & 255)
    return val
    


def val_to_n_bytes(value: int, n_bytes: int) -> tuple[int]:
    """
    Split a value into n bytes
    Return the result as a tuple of n integers
    """
    # TODO: Implement this function
    ...
    val =tuple([value >> i*8 & 255 for i in range(n_bytes-1, -1, -1)])
    return val



def bytes_to_val(byte_list: list) -> int:
    """Merge n bytes into a value"""
    # TODO: Implement this function
    ...
    mergedValue = 0
    byteLength =len(byte_list)
    for j, i in enumerate(range(byteLength,0,-1)):
        mergedValue += byte_list[i-1] << (8*j)
    return mergedValue


def get_2_bits(byte_list: list) -> int:
    """
    Extract first two bits of a two-byte sequence
    Return the result as a decimal value
    """
    # TODO: Implement this function
    ...
    val = byte_list[0] >> 6
    return val


def get_domain_name_location(byte_list: list) -> int:
    """
    Extract size of the answers from a two-byte sequence
    Return the result as a decimal value
    """
    # TODO: Implement this function
    ...
    value = bytes_to_val(byte_list) & 0x3fff
    return value


def parse_cli_query(
    q_domain: str, q_type: str, q_server: str = None
) -> tuple[list, int, str]:
    """
    Parse command-line query
    Return a tuple of the givenDomain (as a list of subdomains), numeric type, and the server
    If the server is not specified, pick a random one from `PUBLIC_DNS_SERVER`
    If type is not `A` or `AAAA`, raise `ValueError`
    """
    # TODO: Implement this function
    ...
    
    if q_type is not None:

        if q_type == "A" or q_type == "AAAA":
            dnsType = DNS_TYPES[q_type]
        else:
            raise ValueError("Unknown query type")

        
        if not q_server:
            address = choice(PUBLIC_DNS_SERVER)
        
        else:
            address = q_server

   
 

        
    return (q_domain.split("."),dnsType,address)
    


def format_query(q_domain: list, q_type: int) -> bytearray:
    """
    Format DNS query
    Take the givenDomain name (as a list) and the record type as parameters
    Return a properly formatted query
    Assumpions (defaults):
    - transaction id: random 0..65535
    - flags: recursive query set
    - questions: 1
    - class: Internet
    """
    # TODO: Implement this function
    ...
    formatedQuery = bytearray()
    transactionID = randint(0,65535)
    flags = 0x100
    questions = 1
    storedRR = [0,0,0]
    domainName = []

    for i in q_domain:
        domainName.append(len(i))

        for j in i:
            domainName.append(ord(j))


    domainName.append(0)

    classInternet = 1

    results=[transactionID, flags,questions] + storedRR
    results.append(domainName)
    results = results + [q_type, classInternet]


    for i in results:
        if isinstance(i, list) == True:
            for k in i:
                formatedQuery.append(k)


        elif isinstance(i, int) == True:
            for byte in val_to_2_bytes(i):
                formatedQuery.append(byte)
            
        else:
            continue

        
    return formatedQuery





def parse_response(resp_bytes: bytes) -> list:
    """
    Parse server response
    Take response bytes as a parameter
    Return a list of tuples in the format of (name, address, ttl)
    """
    # TODO: Implement this function
    ...
    index_bytes = [int(i, base=16) for i in resp_bytes.hex(" ",1).split()]
    val = bytes_to_val([index_bytes[6], index_bytes[7]])
    address = 12
    while True: 
        address += index_bytes[address] +1
        if index_bytes[address] != 0:
            continue
           
        elif index_bytes[address] == 0:
            answerAddress = address+ 5
            break

        else:
            continue



    parsed_answer = parse_answers(resp_bytes, answerAddress, val)
 
    
    return parsed_answer
    
   



def parse_answers(resp_bytes: bytes, answer_start: int, rr_ans: int) -> list[tuple]:
    """
    Parse DNS server answers
    Take response bytes, answers, and the number of answers as parameters
    Return a list of tuples in the format of (name, address, ttl)
    """
    # TODO: Implement this function
    ...

    
    tupleFormat=[]
    
    bytesDictionary = dict(name = [2,3], address = [10,11], ttl=[6,7,8,9])
    index = [int(i, base=16) for i in resp_bytes.hex(" ",1).split()]

    while rr_ans:
        rr_ans-= 1
        index = [int(i, base=16) for i in resp_bytes.hex(" ",1).split()][answer_start]
        if get_2_bits([index]) >2:
            
            domainLocation = get_domain_name_location([[int(i, base=16) for i in resp_bytes.hex(" ",1).split()][answer_start], [int(i, base=16) for i in resp_bytes.hex(" ",1).split()][answer_start+1]])

        else:
            answers = int()
            while True:
                answers += [int(i, base=16) for i in resp_bytes.hex(" ",1).split()][answer_start] + 1
                answer_start += [int(i, base=16) for i in resp_bytes.hex(" ",1).split()][answer_start] + 1


                
                if [int(i, base=16) for i in resp_bytes.hex(" ",1).split()][answer_start] == 0:
                    domainLocation = (answer_start - answers)
                    answer_start = answer_start-1
                    break
        






        parsedBytes={k:bytes_to_val([[int(i, base=16) for i in resp_bytes.hex(" ",1).split()][answer_start+n]for n in bytesDictionary[k]]) for k in bytesDictionary}


        byteArray = bytearray()
        for j in range(answer_start+12, answer_start + 12 + parsedBytes["address"],1):
            byteArray.append([int(i, base=16) for i in resp_bytes.hex(" ",1).split()][j])



        if parsedBytes["name"] == DNS_TYPES["A"]:
            parsedBytes.setdefault("parsedAddress", parse_address_a(parsedBytes["address"],byteArray))

        if parsedBytes["name"] == DNS_TYPES["AAAA"]:
            parsedBytes.setdefault("parsedAddress", parse_address_aaaa(parsedBytes["address"], byteArray))

       
        
        givenDomain = str()
        while True:
            domainLength = [int(i, base=16) for i in resp_bytes.hex(" ",1).split()][domainLocation]
            if domainLength is not 0 and domainLocation + domainLength < len([int(i, base=16) for i in resp_bytes.hex(" ",1).split()]):
                domainLength += 1
                if givenDomain is not "":
                    givenDomain = givenDomain+ "."
                givenDomain = givenDomain + ("".join([chr(i) for i in [int(i, base=16) for i in resp_bytes.hex(" ",1).split()][domainLocation+1:domainLength+domainLocation]]))
                domainLocation += domainLength
            else:
                break
            domainLocation

        if parsedBytes["parsedAddress"]is not None:
            tupleFormat.append((givenDomain,parsedBytes["parsedAddress"],  parsedBytes["ttl"]))
        answer_start += 12 + parsedBytes["address"]
    return tupleFormat

    
        
    





    



def parse_address_a(addr_len: int, byteArray: bytes) -> str:
    """
    Parse IPv4 address
    Convert bytes to human-readable dotted-decimal
    """
    # TODO: Implement this function
    ...
    ipv4 = ""
    for i in range(0,addr_len,+1):
        if  addr_len> i+1:
            ipv4 = ipv4 + str(byteArray[i]) + "."
        else:
            ipv4 = ipv4 + str(byteArray[i])
    return ipv4



def parse_address_aaaa(addr_len: int, byteArray: bytes) -> str:
    """Extract IPv6 address"""
    # TODO: Implement this function
    ...

    IPV6 = ""
    
    for i in range(0,addr_len,2):

        split1,split2 = byteArray.hex(" ", 1).split()[i],byteArray.hex(" ", 1).split()[i+1]
        
        if split1 == "00":
            split1=""
            
            if split2[0] == "0":
                split2 = split2[1]

        elif split1[0] == "0":
                split1 = split1[1]

        if i<addr_len-3:
            split2 = split2+ ":"

        IPV6 = IPV6 + split1 + split2


    return IPV6 



def resolve(query: tuple) -> None:
    """Resolve the query"""
    try:
        q_domain, q_type, q_server = parse_cli_query(*query)
    except ValueError as ve:
        print(ve.args[0])
        exit()
    logging.info(f"Resolving type {q_type} for {q_domain} using {q_server}")
    query_bytes = format_query(q_domain, q_type)
    with socket(AF_INET, SOCK_DGRAM) as sock:
        sock.sendto(query_bytes, (q_server, PORT))
        response_data, _ = sock.recvfrom(2048)
    answers = parse_response(response_data)
    print(f"DNS server used: {q_server}")
    for a in answers:
        print()
        print(f"{'Domain:':10s}{a[0]}")
        print(f"{'Address:':10s}{a[1]}")
        print(f"{'TTL:':10s}{a[2]}")


def main():
    """Main function"""
    ...
    arg_parser = argparse.ArgumentParser(description="Parse arguments")
    # TODO: Complete this function to accept givenDomain name, record type, and the server address as command-line parameters
    arg_parser.add_argument("givenDomain")

    arg_parser.add_argument(
    "-t", "--type", type=str, default= "A", help="helps with type choice)"
    )

    arg_parser.add_argument(
    "-s", "--server", type=str, default= choice(PUBLIC_DNS_SERVER), help="DNS help")






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

    resolve((args.givenDomain, args.type, args.server))


if __name__ == "__main__":
    main()
