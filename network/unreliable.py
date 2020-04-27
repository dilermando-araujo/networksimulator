import copy
import json
import queue
import random
import socket
import threading

from network.packet import MAX_FIELD_VALUE
from network.packet import Packet


class UnreliableDataTransfer:

    def __init__(self, source_addr, destination_addr, loss_probability=0.15, error_probability=0.2):
        if not (0 <= loss_probability <= 1):
            raise Exception("The loss probability must be a value between 0 and 1")
        if not (0 <= error_probability <= 1):
            raise Exception("The error probability must be a value between 0 and 1")

        self.loss_probability = loss_probability
        self.error_probability = error_probability
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(source_addr)
        self.destination_addr = destination_addr
        self.receive_queue = queue.Queue()
        self.listener = threading.Thread(name=f"udt-{source_addr}", target=self.listen, daemon=True)
        self.listener.start()

    def send(self, packet):
        if not isinstance(packet, Packet):
            raise Exception(f"udt_send expects a Packet as parameter, but received a {type(packet)}")

        if len(packet) == 0:
            raise Exception(f"udt_send received an empty Packet")

        print("Transmitting a packet over the unreliable channel")
        packet = copy.deepcopy(packet)

        if random.uniform(0, 1) >= self.loss_probability:
            if random.uniform(0, 1) < self.error_probability:
                field = random.choice(packet.get_available_fields())
                value = packet.get_field(field)
                value += random.randint(0, MAX_FIELD_VALUE - value)
                packet.set_field(field, value)
            bytes_to_send = json.dumps(packet.data).encode()
            self.socket.sendto(bytes_to_send, self.destination_addr)

    def receive(self, timeout=0):
        try:
            return self.receive_queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def listen(self):
        while True:
            data, _ = self.socket.recvfrom(1500)
            print("Received a packet from the unreliable channel")
            packet = Packet(json.loads(data.decode()))
            self.receive_queue.put(packet)
