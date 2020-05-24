from network.packet import Packet
from network.unreliable import UnreliableDataTransfer
from transport import checksum
from datetime import datetime

NUMBER_SEQUENCE = None
PACKET = None

# Para o cálculo do timeout (RTO) [RFC-6298]
# SENDER_RTO = 1
# SENDER_RTTVAR = 0
# SENDER_SRTT = 0

class ReliableDataTransfer:

    def __init__(self, udt):
        if not isinstance(udt, UnreliableDataTransfer):
            raise Exception("udt parameter must be an instance of UnreliableDataTransfer")
        self.udt = udt

    def send(self, payload):

        # global SENDER_RTO
        # global SENDER_RTTVAR
        # global SENDER_SRTT

        packet = Packet({'payload': payload})

        checksum.calculate_checksum(packet)
        stopSend = False
        
        while not stopSend:

            # Inicia o cálculo do RTT atual
            # rtt = (datetime.utcnow().second)

            self.udt.send(packet)
            ack = self.udt.receive(timeout=0.01)
            
            # Recupera o valor do RTT e calcula o RTO.
            # rtt = ((datetime.utcnow().second) - rtt) # Para ficar em segundos
            # if SENDER_SRTT == 0: # Primeira medição
            #     SENDER_SRTT = rtt
            #     SENDER_RTTVAR = rtt / 2
            # else: # Próximas medições
            #     SENDER_RTTVAR = 1 - (1/4) * SENDER_RTTVAR + (1/4) *  SENDER_SRTT - rtt
            #     SENDER_SRTT = 1 - (1/8) * SENDER_SRTT + 1/8 * rtt 
            # SENDER_RTO = SENDER_SRTT + (4 * SENDER_RTTVAR)

            if ack != None:
                if checksum.validate_checksum(ack):
                    if ack.get_field("ACK") == 1:
                        stopSend = True
            # else:
            #     SENDER_RTO = SENDER_RTO * 2
   


    def receive(self):

        global NUMBER_SEQUENCE
        global PACKET

        # Contador que ativa a espera para identificar que o remetente parou de responder.
        KEEP_WAIT = 1
        # Máximo de RTTs que são esperados até identificar que o remetente parou de enviar.
        KEEP_WAIT_MAX = 50

        wait = True
        while wait and KEEP_WAIT <= KEEP_WAIT_MAX:
            packet = self.udt.receive(timeout=0.25)

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
                    KEEP_WAIT = 1

                    nak = Packet()
                    nak.set_field("ACK", 0)

                    checksum.calculate_checksum(nak)
                    print("invalid checksum")
                    self.udt.send(nak)
            else:
                KEEP_WAIT += 1
                if KEEP_WAIT == KEEP_WAIT_MAX:
                    return PACKET.get_field('payload')