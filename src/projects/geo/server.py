#!/usr/bin/env python3
"""
`geo server` implementation

@authors: Frank Lugola
@version: 2022.9
"""
import argparse
from base64 import decode
from itertools import count
import logging
import socket
from csv import DictReader
import csv
from typing import List

HOST = "127.0.0.1"
PORT = 4300

def read_file(filename: str) -> tuple[dict[str, str], int]:
    """Read the world countries and their capitals from the file
    Make sure not to count United States of America and USA as two different countries

    :param filename: file to read
    :return: the tuple of (dictionary, count) where
            `dictionary` is a map {country:capital} and
            `count` is the number of countries in the world
    """

    country_dictionary = {}
    count = 0
    with open(filename) as csvfile:
        csvreader =DictReader(csvfile, delimiter=';')
        for row in csvreader:
            split_countries = list(row["Country"].split(", "))
    
            for i in split_countries:
                capitals = row["Capital"]
                country_dictionary[i] = capitals
            if row["Capital"] not in capitals:
                capitals.add(row["Capital"])
            count +=1
    return country_dictionary, count
    

   
def find_capital(world: dict, country: str) -> str:
    """Find the capital of an existing country
    Return *No such country* otherwise

    :param world: dictionary representing the world
    :param country: country to look up
    :return: capital of the specified country
    """
    world_dictionary = {}
    for key, val in world.items():
        if "," in key:
            key.split(",")
        world_dictionary[key] = val
    
    if country not in world_dictionary:
        return "No such country." 
    
    return world_dictionary.get(country)

def format_message(message: str) -> bytes:
    """Convert the message to bytes

    :param message: message to send
    :return: message converted to bytes
    """
    
    ...
    format_message = message.encode()

    return format_message


def parse_data(data: bytes) -> str:
    """Convert bytes to a string

    :param data: data to decode
    :return: decoded data
    """
   
    ...
    parse_data = data.decode()

    return parse_data


def server_loop(world: dict):
    """Main server loop"""
    print("The server has started")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, PORT))
        while True:
            message, client = sock.recvfrom(2048)
            message = parse_data(message)
            if message == "BYE":
                break
            print(f"Received: {message}")
            sock.sendto(format_message(find_capital(world,message)), client)
        sock.close()
    print("The server has finished")

def main():
    """Main function"""
    arg_parser = argparse.ArgumentParser(description="Enable debugging")
    arg_parser.add_argument("file", type=str, help="File name")
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
    world, _ = read_file(args.file)
    server_loop(world)


if __name__ == "__main__":
    main()
