import datetime
import random
import socket
import struct
import time


class MyTracert():
    def __init__(self, end_point: str, max_steps: int = 20, timeout: int = 3):
        self.max_steps = max_steps
        self.end_point = socket.gethostbyname(end_point)
        self.timeout = timeout
        self.port = random.choice(range(33434, 33535))
        self.sender = self._create_sender_socket()
        self.receiver = self._create_receiver_socket()
        self.message = b"hello"

    def _construct_message(self, connection_time, address):
        try:
            name = socket.gethostbyaddr(address[0])[0]
        except socket.error:
            name = address[0]
        return "address: " + str(name) + "connection_time: " + str(connection_time)

    def _create_sender_socket(self):
        proto_udp = socket.getprotobyname("udp")
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, proto_udp)
        # creating a datagram oriented socket with (host, port) address format and udp protocol
        return sender_socket

    def _create_receiver_socket(self):
        proto_icmp = socket.getprotobyname("icmp")
        icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, proto_icmp)
        # creating a socket with (host, port) address format and opportunities to read/create headers
        # using tcmp protocol
        icmp_socket.bind(('', self.port))  # binding socket to random port
        icmp_socket.settimeout(self.timeout)
        return icmp_socket

    def _send_package(self, ttl: int):
        self.sender.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)  # changing the time of life
        self.sender.sendto(''.encode(), (socket.gethostbyname(self.end_point), self.port))

    def _receive_answer(self):
        try:
            addr = self.receiver.recvfrom(512)[1]  # returns a pair -- (bytes, address)
        except socket.error as e:
            print(' smth went wrong ', str(e))
            addr = '*'
        return addr

    def tracert_run(self):
        try:
            dest_address = socket.gethostbyname(self.end_point)
        except socket.error:
            print("Unknown destination")
            return -1
        for ttl in range(1, self.max_steps + 1):
            begin = datetime.datetime.now()
            self._send_package(ttl)
            cur_address = self._receive_answer()
            end = datetime.datetime.now()
            connect_time = end - begin
            print(self._construct_message(connect_time, cur_address))
            if cur_address[0] == dest_address:
                break
        print('the address seems to be too far away')
        return 0



