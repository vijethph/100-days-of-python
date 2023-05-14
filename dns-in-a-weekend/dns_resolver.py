"""Module to resolve DNS response to figure out IP address
This is part of a collection of Python scripts to implement a toy DNS resolver
Credits and Attributions: Julia Evans (https://implement-dns.wizardzines.com/index.html)
"""

import socket
from dns_query_builder import build_query, TYPE_A, TYPE_NS
from dns_response_parser import parse_dns_packet


def send_query(ip_address, domain_name, record_type):
    """sends a DNS query"""
    query = build_query(domain_name, record_type)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(query, (ip_address, 53))

    data, _ = sock.recvfrom(1024)
    return parse_dns_packet(data)


def get_answer(packet):
    """returns the first A record in the Answer section"""
    for record_answer in packet.answers:
        if record_answer.type_ == TYPE_A:
            return record_answer.data
    return None


def get_nameserver_ip(packet):
    """returns the first A record in the Additional section"""
    for record_additional in packet.additionals:
        if record_additional.type_ == TYPE_A:
            return record_additional.data
    return None


def get_nameserver(packet):
    """returns the first NS record in the Authority section"""
    for record_authority in packet.authorities:
        if record_authority.type_ == TYPE_NS:
            return record_authority.data.decode("utf-8")
    return None


def resolve(domain_name, record_type):
    """DNS resolver"""
    nameserver = "198.41.0.4" # IP address of one of the root nameservers
    while True:
        print(f"Querying {nameserver} for {domain_name}")
        response = send_query(nameserver, domain_name, record_type)
        if ip_address := get_answer(response):
            return ip_address
        elif ns_ip := get_nameserver_ip(response):
            nameserver = ns_ip
        # New case: look up the nameserver's IP address if there is one
        elif ns_domain := get_nameserver(response):
            nameserver = resolve(ns_domain, TYPE_A)
        else:
            raise Exception("something went wrong")
