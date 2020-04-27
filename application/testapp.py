import sys

from transport.reliable import ReliableDataTransfer


class SingleDirectionTestApp:

    def __init__(self, rdt, num_packets, name):
        if not isinstance(rdt, ReliableDataTransfer):
            raise Exception("rdt parameter must be an instance of ReliableDataTransfer")
        self.rdt = rdt
        self.num_packets = num_packets
        self.name = name

    def send_data(self):
        for i in range(self.num_packets):
            print(f"Test app {self.name} sending packet {i}")
            self.rdt.send(i)

        print("ALL DATA HAS BEEN SENT!!!")

    def receive_data(self):
        for i in range(self.num_packets):
            received = self.rdt.receive()
            if received == i:
                print(f"Test app {self.name} received packet {i}")
            else:
                print(f"Test app {self.name} received an invalid data. Expected value {i}, got {received}")
                sys.exit(1)

        print("ALL DATA HAS BEEN RECEIVED!!!")
