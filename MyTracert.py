import random
import socket
import struct
import time


class MyTracert():

    def __init__(self, end_point: str, max_steps: int = 20):
        self.max_steps = max_steps
        self.end_point = end_point
        self.port = random.random()
        self.sender = self._create_sender_socket()
        self.receiver = self._create_receiver_socket()
        self.message = b"hello"


    def construct_message(self, connection_time, address):
        try:
            name = socket.gethostbyaddr(address[0])[0]
        except socket.error:
            name = address[0]
        return "address: " + str(name) + "connection_time: " + str(connection_time)

    def _create_sender_socket(self):
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # creating a datagram oriented socket with (host, port) address format and udp protocol
        return sender_socket

    def _create_receiver_socket(self):
        icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        # creating a socket with (host, port) address format and opportunities to read/create headers
        # and tcmp protocol
        icmp_socket.bind(('', self.port))  # binding port to icmp socket

        timeout_value = struct.pack('@ll', 3, 0)
        icmp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout_value)
        # set timeout flag on the socket level
        return icmp_socket

    def send_package(self, ttl: int):
        self.sender.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)  # changing the time of life
        self.sender.sendto(self.message, (self.end_point, self.port))

    def receive_answer(self):
        return self.receiver.recvfrom(1024)[1]  # returns a pair -- (bytes, address)

    def run(self):
        try:
            dest_address = socket.gethostbyname(self.end_point)
        except socket.error:
            print("Unknown destination")
            return -1
        for ttl in range(1, self.max_steps + 1):
            begin = time.perf_counter_ns()
            self.send_package(ttl)
            cur_address = self.receive_answer()
            end = time.perf_counter_ns()
            connect_time = end - begin
            print(self.construct_message(connect_time, cur_address))
            if cur_address[0] == dest_address:
                return 0

        print('the address seems to be too far away')
        return 0



