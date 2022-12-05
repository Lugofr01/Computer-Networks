#!/usr/bin/env python3
"""
Python traceroute implementation using ICMP
"""


"""
@author:Frank Charles Lugola
@version: 2022.10
"""
import argparse
import logging
import os
import socket
import struct
import time

ATTEMPTS = 3
ECHO_REQUEST_CODE = 0
ECHO_REQUEST_TYPE = 8



def checksum(pkt_bytes: bytes) -> int:
    """
    Calculate checksum
    :param pkt_bytes: packet bytes
    :returns checksum as an integer
    """
    chksum = 0
    if len(pkt_bytes) % 2:
        pkt_bytes += b"\00"

    for i in range(0, len(pkt_bytes), 2):
        word = (pkt_bytes[i] << 8) + pkt_bytes[i + 1]
        chksum = ((chksum + word) & 0xFFFF) + ((chksum + word) >> 16)

    return ~chksum & 0xFFFF

def receive_reply(sock: socket) -> tuple:
    """
    Receive an ICMP reply
    :param sock: socket to use
    :returns a tuple of the received packet bytes, responder's address, and current time
    """
    pkt_bytes, addr = sock.recvfrom(1024)
    return pkt_bytes, addr, time.time()

def parse_reply(pkt_bytes: bytes) -> None:
    """
    Parse an ICMP reply
    :param pkt_bytes: data received from the wire
    """
    header = pkt_bytes[20:28]
    data = pkt_bytes[28:]
    expected_types_and_codes = {0: [0], 3: [0, 1, 3], 8: [0], 11: [0]}

    repl_type, repl_code, repl_checksum, repl_id, sequence = struct.unpack("!BBHHH", header)

    if repl_type not in expected_types_and_codes:
         raise ValueError(f"Incorrect type {repl_type} received " + f"instead of {', '.join([str(t) for t in expected_types_and_codes])}")

    if repl_code not in expected_types_and_codes[repl_type]:
        raise ValueError(f"Incorrect code {repl_code} received with type {repl_type}")

    if checksum(header + data) != 0:
        raise ValueError( f"Incorrect checksum {repl_checksum:04x} received " + f"instead of {checksum(header + data):04x}")


def bytes_to_str(pkt_bytes: bytes) -> str:
    """
    Convert packet bytes to a printable string
    :param pkt_bytes: data received from the wire
    :returns string with hexadecimal values of raw bytes
    """
    result = []
    for i, val in enumerate(pkt_bytes):
        if (i + 1) % 16 == 0:
            result.append("\n")
        elif (i + 1) % 8 == 0:
            result.append("  ")
        else:
            result.append(" ")
        result.append(f"{val:02x}")
    result.append("\n")
    result.append("\n")
    return "".join(result)


<<<<<<< HEAD
def format_request(req_id: int, seq_num: int) -> bytes:
    """
    Format an Echo request
=======


















                            f"{socket.gethostbyaddr(resp_addr[0])[0]} [{resp_addr[0]}]"
                        )
                        comment
                        comment = (
                        comment = resp_addr[0]
                        comment if comment else f"Request timed out: {str(to_err)}"
                        else f"Error while parsing the response: {str(val_err)}"
                        if comment
                    )
                    )
                    comment = (
                    comment = (
                    continue
                    continue
                    destination_reached = True
                    except socket.herror:
                    parse_reply(pkt_in)
                    pkt_in, resp_addr, time_rcvd = receive_reply(sock)
                    print(f"{'!':>3s}      ", end="")
                    print(f"{'*':>3s}      ", end="")
                    print(f"{'<1':>3s} ms   ", end="")
                    print(f"{rtt:>3.0f} ms   ", end="")
                    try:
                else:
                except (socket.timeout, TimeoutError) as to_err:
                except ValueError as val_err:
                if not comment:
                if resp_addr[0] == dest_addr:
                if rtt > 1:
                pkt_out = format_request(req_id, seq_id)
                rtt = (time_rcvd - time_sent) * 1000
                seq_id += 1
                time_sent = send_request(sock, pkt_out, dest_addr, ttl)
                try:
            + f"instead of {', '.join([str(t) for t in expected_types_and_codes])}"
            + f"instead of {checksum(header + data):04x}"
            comment = ""
            f"Incorrect checksum {repl_checksum:04x} received "
            f"Incorrect type {repl_type} received "
            for _ in range(ATTEMPTS):
            print(comment)
            print(f"{ttl:>3d}   ", end="")
            result.append("  ")
            result.append(" ")
            result.append("\n")
            seq_id = 0
            ttl += 1
        "-d", "--debug", action="store_true", help="Enable logging.DEBUG mode"
        "!BBHHH",
        "!BBHHH",
        "!BBHHH", header
        )
        )
        + f"over a maximum of {max_hops} hops\n"
        0,
        checksum(header + data),
        chksum = ((chksum + word) & 0xFFFF) + ((chksum + word) >> 16)
        destination_reached = False
        ECHO_REQUEST_CODE,
        ECHO_REQUEST_CODE,
        ECHO_REQUEST_TYPE,
        ECHO_REQUEST_TYPE,
        elif (i + 1) % 8 == 0:
        else:
        f"\nTracing route to {hostname} [{dest_addr}]\n"
        if (i + 1) % 16 == 0:
        logger.setLevel(logging.DEBUG)
        logger.setLevel(logging.WARNING)
        pkt_bytes += b"\00"
        raise ValueError(
        raise ValueError(
        raise ValueError(f"Incorrect code {repl_code} received with type {repl_type}")
        req_id,
        req_id,
        result.append(f"{val:02x}")
        seq_num,
        seq_num,
        sock.settimeout(1)
        socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp")
        ttl = 0
        while ttl < max_hops and not destination_reached:
        word = (pkt_bytes[i] << 8) + pkt_bytes[i + 1]
    :param addr_dst: destination address
    :param hostname: host name
    :param max_hops: max hops
    :param pkt_bytes: data received from the wire
    :param pkt_bytes: data received from the wire
    :param pkt_bytes: packet bytes
    :param pkt_bytes: packet bytes to send
>>>>>>> b463ff3dcae9ca1bb433108d634e6159088a47de
    :param req_id: request id
    :param seq_num: sequence number
    :returns properly formatted Echo request
    :returns string with hexadecimal values of raw bytes
    """
    """
    """
    data = b"VOTE!"
    header = struct.pack( "!BBHHH",  ECHO_REQUEST_TYPE, ECHO_REQUEST_CODE, 0, req_id, seq_num,)
    header = struct.pack( "!BBHHH",  ECHO_REQUEST_TYPE, ECHO_REQUEST_CODE, checksum(header + data), req_id, seq_num,)
    return header + data

def send_request(sock: socket, pkt_bytes: bytes, addr_dst: str, ttl: int) -> float:
    """
    Send an Echo Request
    :param sock: socket to use
    :param pkt_bytes: packet bytes to send
    :param addr_dst: destination address
    :param ttl: ttl of the packet
    :returns current time
    """
    sock.sendto(pkt_bytes, (addr_dst, 33434))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack("I", ttl))
    return time.time()

def traceroute(hostname: str, max_hops: int = 30) -> None:
    """
    Trace the route to a domain
    :param hostname: host name
    :param max_hops: max hops
    """
    dest_addr = socket.gethostbyname(hostname)
    print(f"\nTracing route to {hostname} [{dest_addr}]\n" + f"over a maximum of {max_hops} hops\n")
    req_id = os.getpid() & 0xFFFF
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp")) as sock:
        ttl = 0
        sock.settimeout(1)
        destination_reached = False
        while ttl < max_hops and not destination_reached:
            seq_id = 0
            ttl += 1
            comment = ""
            print(f"{ttl:>3d}   ", end="")
            for _ in range(ATTEMPTS):
                seq_id += 1
                pkt_out = format_request(req_id, seq_id)
                time_sent = send_request(sock, pkt_out, dest_addr, ttl)
                try:
                    pkt_in, resp_addr, time_rcvd = receive_reply(sock)
                    parse_reply(pkt_in)
                
                except (socket.timeout, TimeoutError) as to_err:
                    print(f"{'*':>3s}", end="")
                    comment = (comment if comment else f"Request timed out: {str(to_err)}")
                    continue
                except ValueError as val_err:
                    print(f"{'!':>3s}", end="")
                    comment = (comment if comment else f"Error while parsing the response: {str(val_err)}")
                    continue
                rtt = (time_rcvd - time_sent) * 1000
                if rtt > 1:
                    print(f"{rtt:>3.0f} ms   ", end="")
                else:
                    print(f"{'<1':>3s} ms   ", end="")
                if not comment:
                    try:
                        comment = (f"{socket.gethostbyaddr(resp_addr[0])[0]} [{resp_addr[0]}]")
                    except socket.herror:
                        comment = resp_addr[0]
                if resp_addr[0] == dest_addr:
                    destination_reached = True
            
            print(comment)     
    print("\nTrace complete.")


def main():
    """Main function"""
    arg_parser = argparse.ArgumentParser(description="Parse arguments")
<<<<<<< HEAD
    arg_parser.add_argument("host", type=str, help="Host to trace")
    arg_parser.add_argument("-d", "--debug", action="store_true", help="Enable logging.DEBUG mode")
    
    args = arg_parser.parse_args()
    logger = logging.getLogger("root")
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logger.level)
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)

    traceroute(args.host)

if __name__ == "__main__":
    main()

=======
    arg_parser.add_argument(
    arg_parser.add_argument("host", type=str, help="Host to trace")
    args = arg_parser.parse_args()
    Calculate checksum
    chksum = 0
    Convert packet bytes to a printable string
    data = b"VOTE!"
    data = pkt_bytes[28:]
    dest_addr = socket.gethostbyname(hostname)
    else:
    expected_types_and_codes = {0: [0], 3: [0, 1, 3], 8: [0], 11: [0]}
    for i in range(0, len(pkt_bytes), 2):
    for i, val in enumerate(pkt_bytes):
    Format an Echo request
    header = pkt_bytes[20:28]
    header = struct.pack(
    header = struct.pack(
    if args.debug:
    if checksum(header + data) != 0:
    if len(pkt_bytes) % 2:
    if repl_code not in expected_types_and_codes[repl_type]:
    if repl_type not in expected_types_and_codes:
    logger = logging.getLogger("root")
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logger.level)
    main()
    Parse an ICMP reply
    pkt_bytes, addr = sock.recvfrom(1024)
    print(
    print("\nTrace complete.")
    Receive an ICMP reply
    repl_type, repl_code, repl_checksum, repl_id, sequence = struct.unpack(
    req_id = os.getpid() & 0xFFFF
    result = []
    result.append("\n")
    result.append("\n")
    return "".join(result)
    return ~chksum & 0xFFFF
    return header + data
    return pkt_bytes, addr, time.time()
    return time.time()
    Send an Echo Request
    sock.sendto(pkt_bytes, (addr_dst, 33434))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack("I", ttl))
    Trace the route to a domain
    traceroute(args.host)
    with socket.socket(
"""
"""
@author:
@version: 2022.10
#!/usr/bin/env python3
ATTEMPTS = 3
def bytes_to_str(pkt_bytes: bytes) -> str:
def checksum(pkt_bytes: bytes) -> int:
def format_request(req_id: int, seq_num: int) -> bytes:
def main():
def parse_reply(pkt_bytes: bytes) -> None:
def receive_reply(sock: socket) -> tuple:
def send_request(sock: socket, pkt_bytes: bytes, addr_dst: str, ttl: int) -> float:
def traceroute(hostname: str, max_hops: int = 30) -> None:
ECHO_REQUEST_CODE = 0
ECHO_REQUEST_TYPE = 8
if __name__ == "__main__":
import argparse
import logging
import os
import socket
import struct
import time
Python traceroute implementation using ICMP
>>>>>>> b463ff3dcae9ca1bb433108d634e6159088a47de
