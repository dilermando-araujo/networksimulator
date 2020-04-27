from network.packet import Packet


def sum_words(words):
    sum = 0

    for i, word in enumerate(words):
        sum += word

    sum_16bit = sum & 0xFFFF
    return sum_16bit


def get_1s_complement(value):
    return ~value & 0xFFFF


def calculate_checksum(packet):
    if not isinstance(packet, Packet):
        raise Exception("packet must be instance of Packet class")

    fields = packet.get_available_field_values()
    sum = sum_words(fields)
    checksum = get_1s_complement(sum)

    packet.set_field("CHECKSUM", checksum)
    return checksum


def validate_checksum(packet):
    if not isinstance(packet, Packet):
        raise Exception("packet must be instance of Packet class")

    fields = packet.get_available_field_values()
    return sum_words(fields) == 0xFFFF
