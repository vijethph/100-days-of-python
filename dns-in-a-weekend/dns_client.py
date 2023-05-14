"""Module to perform DNS query
This is part of a collection of Python scripts to implement a toy DNS resolver
Credits and Attributions: Julia Evans (https://implement-dns.wizardzines.com/index.html)
"""

import socket
from io import BytesIO
from dns_query_builder import build_query, TYPE_A
from dns_response_parser import parse_header, parse_question, parse_record, parse_dns_packet, lookup_domain
from dns_resolver import resolve

"""Optional Part to lookup domains using 8.8.8.8 DNS resolver

query = build_query("www.example.com", 1)

# create a UDP socket
# `socket.AF_INET` means that we're connecting to the internet
#                  (as opposed to a Unix domain socket `AF_UNIX` for example)
# `socket.SOCK_DGRAM` means "UDP"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send our query to 8.8.8.8, port 53. Port 53 is the DNS port.
sock.sendto(query, ("8.8.8.8", 53))

# read the response. UDP DNS responses are usually less than 512 bytes
# (see https://www.netmeister.org/blog/dns-size.html for MUCH more on that)
# so reading 1024 bytes is enough
response, _ = sock.recvfrom(1024)

# BytesIO lets us keep a pointer to the current position in a byte stream and lets you read from it and advance the pointer
reader = BytesIO(response)
parse_header(reader)
parse_question(reader)
parse_record(reader)
packet = parse_dns_packet(response)
lookup_domain("example.com")

"""

response = resolve("yahoo.com", TYPE_A)
print(response)
