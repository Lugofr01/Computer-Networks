#!/usr/bin/env python3
"""Router implementation using UDP sockets"""

# Frank Lugola 
# route
import argparse
import logging
import pathlib
import random
import select
import socket
import struct
import time
import toml
from typing import Tuple, Set, Dict


THIS_HOST = None
BASE_PORT = 4300


def read_config_file(filename: str) -> Tuple[Set, Dict]:
    """
    Read config file

    :param filename: name of the configuration file
    :return tuple of the (neighbors, routing table)
    """

    try:
        
        with open(filename,"r") as reader:
            config = [position for position in reader.readlines() if position.strip()]
            address = False
            storeDict = {}
            for index in config:
                position = index.split()
                if len(position) == 1:
                    indexEnding = index.endswith("{}\n".format(THIS_HOST))
                    if not indexEnding:
                        address = False
                    else:
                        address = True
                if len(position) == 2 and address is True:
                    storeDict[position[0]] = [int(position[1]),position[0]]

            return set(storeDict.keys()), storeDict

    except:
        raise FileNotFoundError("Could not find the specified configuration file {}".format(filename))
    
    
###################################################

def format_update(routing_table: dict) -> bytes:
    """
    Format update message

    :param routing_table: routing table of this router
    :returns the formatted message
    """

    routerTable=[]
    formattedMessage = b'\x00'
    for i in routing_table:
        routeList =list(map(int,(routing_table[i][1]).split(".")))+[routing_table[i][0]]
        routerTable.append(routeList)
    for j in routerTable:
        formattedMessage += bytearray(j)
    return formattedMessage

# ####################################
def parse_update(msg: bytes, neigh_addr: str, routing_table: dict) -> bool:
    """
    Update routing table
    
    :param msg: message from a neighbor
    :param neigh_addr: neighbor's address
    :param routing_table: this router's routing table
    :returns True is the table has been updated, False otherwise
    """
###############################
    cost = routing_table[neigh_addr][0]
    messageArray = []
    updates= False
    parsedMessage = struct.unpack("{}B".format(len(msg)-1),msg[1:len(msg)])
    def helper(address):
        strAddress =".".join([str(n) for n in address])
        return strAddress
    
    for i in range(0, len(parsedMessage),+5):
        messageArray.append([parsedMessage[i+4]+cost,helper(parsedMessage[i:i+4])])

    for j in messageArray:
        if j[1] in routing_table:
            if routing_table[j[1]][0] > j[0]:
                routing_table[j[1]] = [j[0],neigh_addr]
                updates= True


            else:
                updates=False

        elif j[1] != THIS_HOST:
            routing_table[j[1]] = [j[0],neigh_addr]
            updates= True

    return updates


def send_update(routing_table: dict, node: str) -> None:
    """
    Send update
    
    :param node: recipient of the update message
    """
   #################################
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((THIS_HOST, BASE_PORT))
        sock.sendto(format_update(routing_table), (node, BASE_PORT + int(node[-1])))
   



def format_hello(msg_txt: str, src_node: str, dst_node: str) -> bytes:
    """
    Format hello message
    
    :param msg_txt: message text
    :param src_node: message originator
    :param dst_node: message recipient
  
    """
    #################
    messageOriginator = list(map(int,src_node.split(".")+dst_node.split(".")))
    return bytearray([1]+ messageOriginator) + msg_txt.encode()


def parse_hello(msg: bytes, routing_table: dict) -> str:
    """
    Parse the HELLO message

    :param msg: message
    :param routing_table: this router's routing table
    :returns the action taken as a string
    """
#################
    def helper(address):
        strAddress =".".join([str(n) for n in address])
        return strAddress
    sourceDestination = [helper(struct.unpack("4B",msg[1:5])),helper(struct.unpack("4B",msg[5:9]))]
    decodedMessage = msg[9:].decode()
    operation = []

    if sourceDestination[1] == THIS_HOST:
        operation += ["Received "," from ",sourceDestination[0]]
    else:
        send_hello(decodedMessage, sourceDestination[0], sourceDestination[1], routing_table)
        operation =operation+ ["Forwarded "," to ",sourceDestination[1]]

    return operation[0] +decodedMessage + operation[1] + operation[2]


def send_hello(msg_txt: str, src_node: str, dst_node: str, routing_table: dict) -> None:
    """
    Send a message

    :param mst_txt: message to send
    :param src_node: message originator
    :param dst_node: message recipient
    :param routing_table: this router's routing table
    """

# ##########################################
    def helper2(address):
        return int(address.split(".")[3])+BASE_PORT
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((THIS_HOST, BASE_PORT))
        sock.sendto(format_hello(msg_txt, src_node, dst_node), (routing_table[dst_node][1], helper2(routing_table[dst_node][1])))

def print_status(routing_table: dict) -> None:

    """
    Print status

    :param routing_table: this router's routing table
    """
#############################
    print("{:^10}{:^10}{:^10}".format("Host","Cost","Via"))
    for i in routing_table:
        print("{:^10}{:^10}{:^10}".format(i, routing_table[i][0], routing_table[i][1]))


def route(neighbors: set, routing_table: dict, timeout: int = 5):
    """
    Router's main loop

    :param neighbors: this router's neighbors
    :param routing_table: this router's routing table
    :param timeout: default 5
    """
    ubuntu_release = [
        "Groovy Gorilla",
        "Focal Fossa",
        "Eoam Ermine",
        "Disco Dingo",
        "Cosmic Cuttlefish",
        "Bionic Beaver",
        "Artful Aardvark",
        "Zesty Zapus",
        "Yakkety Yak",
        "Xenial Xerus",
    ]
   
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((THIS_HOST, BASE_PORT + int(THIS_HOST[-1])))


    time.sleep(random.randint(1, 4))

    # sending update 
    for i in neighbors:
        send_update(routing_table, i)
    print_status(routing_table)
    


    while [sock]:
        message, _, _ = select.select([sock], [], [], timeout)
        if random.randint(0,100) > 10:
            for _ in message:
                packetReeceived, addr = sock.recvfrom(2048)
                if packetReeceived[0] == 0:
                    time.sleep(random.randint(1, 4))
                    updated = parse_update(packetReeceived, addr[0], routing_table)
                    for i in neighbors:
                        send_update(routing_table, i)
                    print_status(routing_table)
                    time.sleep(random.randint(1, 4))
            
                   
                elif packetReeceived[0] == 1:
                     print(parse_hello(packetReeceived, routing_table))
                    
        else:
            time.sleep(random.randint(1, 4))
            send_hello(random.choice(ubuntu_release), THIS_HOST, str(random.choice(list(neighbors))), routing_table)
            time.sleep(random.randint(1, 4))
            
    sock.close()

def main():
    """Main function"""


    arg_parser = argparse.ArgumentParser(description="Parse arguments")
    arg_parser.add_argument("-c", "--debug", action="store_true", help="Enable logging.DEBUG mode")
    arg_parser.add_argument("filepath", type=str, help="file path")
    arg_parser.add_argument("address", type=str, help="client src")
    args = arg_parser.parse_args()

    logger = logging.getLogger("root")
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logger.level)
    
    global THIS_HOST 
    THIS_HOST = args.address
    route(read_config_file(args.filepath)[0], read_config_file(args.filepath)[1], timeout=5)

    


if __name__ == "__main__":
    main()


# done