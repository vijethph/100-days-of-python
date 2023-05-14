"""Module to build DNS Query
This is part of a collection of Python scripts to implement a toy DNS resolver
Credits and Attributions: Julia Evans (https://implement-dns.wizardzines.com/index.html)
"""

from dataclasses import dataclass
import dataclasses
import struct
import random

random.seed(1)

TYPE_A = 1
TYPE_NS = 2
CLASS_IN = 1


@dataclass
class DNSHeader:
    """DNS queries have 2 parts: a header and a question. This is DNS Header class"""

    header_id: int
    flags: int
    # the below variables represent how many records to expect in each section of a DNS packet
    num_questions: int = 0
    num_answers: int = 0
    num_authorities: int = 0
    num_additionals: int = 0


@dataclass
class DNSQuestion:
    """DNS Question class"""

    name: bytes
    type_: int  # type is a built-in function in Python
    class_: int  # class is a reserved word in Python


def header_to_bytes(header):
    """converts DNS headers to byte strings"""
    fields = dataclasses.astuple(header)
    # there are 6 `H`s because there are 6 fields
    return struct.pack("!HHHHHH", *fields)


def question_to_bytes(question):
    """converts DNS questions to byte strings"""
    return question.name + struct.pack("!HH", question.type_, question.class_)


def encode_dns_name(domain_name):
    """encodes the domain name"""
    encoded = b""
    for part in domain_name.encode("ascii").split(b"."):
        encoded += bytes([len(part)]) + part
    return encoded + b"\x00"


def build_query(domain_name, record_type):
    """constructs DNS Query"""
    name = encode_dns_name(domain_name)
    header_id = random.randint(0, 65535)
    header = DNSHeader(header_id=header_id, num_questions=1, flags=0)
    question = DNSQuestion(name=name, type_=record_type, class_=CLASS_IN)
    return header_to_bytes(header) + question_to_bytes(question)
