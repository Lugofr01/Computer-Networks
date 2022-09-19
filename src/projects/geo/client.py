#!/usr/bin/env python3
"""
`geo client` implementation

@authors:Frank Lugola

@version: 2022.9
"""
import argparse
from email.message import Message
import logging
import socket

HOST = "localhost"
PORT = 4300


def format_message(message: list[str]) -> bytes:
    """Convert the message to bytes

    :param message: message to encode
    :return: message as bytes
    """

    ...
    format_message = message.encode()

    return format_message


def parse_data(data: bytes) -> str:
    """Convert bytes to a string

    :param data: data received
    :return: decoded string
    """
    
    ...
    parse_data = data.decode()


    return parse_data


def read_user_input() -> str:
    """Read user input from the console

    :return: country name
    """
   
    ...
    read_user_input = input("Enter a Country name: ")

    return read_user_input



def client_loop():
    """Main client loop"""
    print("The client has started")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        while True:
            message = read_user_input()
            logging.info("Connecting to %s:%d", HOST, PORT)
            logging.info("Connected to %s:%d", HOST, PORT)
            logging.info("Formatting data")
            sock.sendto(format_message(message), (HOST, PORT))
            if message == "BYE":
                break
            outData, _ = sock.recvfrom(2048)
            message = parse_data(outData)
            print(message)
            print(f"Recieved: {message}")
    print("The client has finished")


def main():
    """Main function"""
    arg_parser = argparse.ArgumentParser(description="Enable debugging")
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
    client_loop()


if __name__ == "__main__":
    main()
