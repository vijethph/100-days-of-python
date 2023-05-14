"""Module to parse the response to the DNS Query
This is part of a collection of Python scripts to implement a toy DNS resolver
Credits and Attributions: Julia Evans (https://implement-dns.wizardzines.com/index.html)
"""

from dataclasses import dataclass
from typing import List
from io import BytesIO
import struct
import socket
from dns_query_builder import DNSQuestion, DNSHeader, build_query, TYPE_A, TYPE_NS


@dataclass
class DNSRecord:
    """DNS Record class"""

    name: bytes
    type_: int
    class_: int
    ttl: int
    data: bytes


@dataclass
class DNSPacket:
    """DNS Packet class"""

    header: DNSHeader
    questions: List[DNSQuestion]
    answers: List[DNSRecord]
    authorities: List[DNSRecord]
    additionals: List[DNSRecord]


def parse_header(reader):
    """parses the DNS Header"""
    items = struct.unpack("!HHHHHH", reader.read(12))
    return DNSHeader(*items)


def decode_name_simple(reader):
    """decodes domain name (simple version)"""
    parts = []
    while (length := reader.read(1)[0]) != 0:
        parts.append(reader.read(length))
    return b".".join(parts)


def parse_question(reader):
    """parses the DNS Question"""
    name = decode_name_simple(reader)
    data = reader.read(4)
    type_, class_ = struct.unpack("!HH", data)
    return DNSQuestion(name, type_, class_)


def decode_name(reader):
    """decodes the domain name"""
    parts = []
    while (length := reader.read(1)[0]) != 0:
        if length & 0b1100_0000:
            parts.append(decode_compressed_name(length, reader))
            break
        parts.append(reader.read(length))
    return b".".join(parts)


def decode_compressed_name(length, reader):
    """decodes compressed version of domain name"""
    pointer_bytes = bytes([length & 0b0011_1111]) + reader.read(1)
    pointer = struct.unpack("!H", pointer_bytes)[0]
    current_pos = reader.tell()
    reader.seek(pointer)
    result = decode_name(reader)
    reader.seek(current_pos)
    return result


def parse_record(reader):
    """parses the DNS record"""
    name = decode_name(reader)
    data = reader.read(10)
    type_, class_, ttl, data_len = struct.unpack("!HHIH", data)
    if type_ == TYPE_NS:
        data = decode_name(reader)
    elif type_ == TYPE_A:
        data = ip_to_string(reader.read(data_len))
    else:
        data = reader.read(data_len)
    return DNSRecord(name, type_, class_, ttl, data)


def parse_dns_packet(data):
    """parses the DNS packet"""
    reader = BytesIO(data)
    header = parse_header(reader)
    questions = [parse_question(reader) for _ in range(header.num_questions)]
    answers = [parse_record(reader) for _ in range(header.num_answers)]
    authorities = [parse_record(reader) for _ in range(header.num_authorities)]
    additionals = [parse_record(reader) for _ in range(header.num_additionals)]

    return DNSPacket(header, questions, answers, authorities, additionals)


def ip_to_string(ip_address):
    """converts IP address numbers in array to a string"""
    return ".".join([str(x) for x in ip_address])


def lookup_domain(domain_name):
    """performs DNS query to lookup IP addresses for a domain name"""
    query_obj = build_query(domain_name, TYPE_A)
    socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_obj.sendto(query_obj, ("8.8.8.8", 53))

    # get the response
    data, _ = socket_obj.recvfrom(1024)
    dns_response = parse_dns_packet(data)
    return ip_to_string(dns_response.answers[0].data)
