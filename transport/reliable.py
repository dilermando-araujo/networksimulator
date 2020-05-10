from network.packet import Packet
from network.unreliable import UnreliableDataTransfer
from transport import checksum

NUMBER_SEQUENCE = None
PACKET = None

class ReliableDataTransfer:

    def __init__(self, udt):
        if not isinstance(udt, UnreliableDataTransfer):
            raise Exception("udt parameter must be an instance of UnreliableDataTransfer")
        self.udt = udt

    def send(self, payload):
        print("PRINT")
        packet = Packet({'payload': payload})

        checksum.calculate_checksum(packet)
        stopSend = False
        
        while not stopSend:
            self.udt.send(packet)
            ack = self.udt.receive(timeout=5)
            
            if checksum.validate_checksum(ack):
                if ack.get_field("ACK") == 1:
                    stopSend = True
   


    def receive(self):

        global NUMBER_SEQUENCE
        global PACKET

        wait = True
        while wait:
            packet = self.udt.receive(timeout=5)

            if packet != None:
                valid = checksum.validate_checksum(packet)
                if valid:
                    if NUMBER_SEQUENCE == None:
                        NUMBER_SEQUENCE = packet.get_field("payload")
                        PACKET = packet

                    ack = Packet()
                    ack.set_field("ACK", 1)

                    checksum.calculate_checksum(ack)
                    self.udt.send(ack)

                    if (NUMBER_SEQUENCE + 1) == packet.get_field("payload"):
                        LAST_PACKET = PACKET
                        NUMBER_SEQUENCE += 1
                        PACKET = packet
                        return LAST_PACKET.get_field("payload")
                else:
                    nak = Packet()
                    nak.set_field("ACK", 0)

                    checksum.calculate_checksum(nak)
                    print("invalid checksum")
                    self.udt.send(nak)
            else:
                return PACKET.get_field('payload')