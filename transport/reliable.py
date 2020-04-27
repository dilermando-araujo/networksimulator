from network.packet import Packet
from network.unreliable import UnreliableDataTransfer
from transport import checksum


class ReliableDataTransfer:

    def __init__(self, udt):
        if not isinstance(udt, UnreliableDataTransfer):
            raise Exception("udt parameter must be an instance of UnreliableDataTransfer")
        self.udt = udt

    def send(self, payload):
        packet = Packet({'payload': payload})
        checksum.calculate_checksum(packet)
        self.udt.send(packet)
        # should wait for ACK before returning
        # if some time has passed while waiting for ACK, then it should retransmit the packet

    def receive(self):
        packet = self.udt.receive(timeout=1)
        # should wait until there's data coming from bottom layer
        valid = checksum.validate_checksum(packet)
        if valid:
            # should acknowledge sender
            return packet.get_field('payload')
        else:
            print("invalid checksum")
