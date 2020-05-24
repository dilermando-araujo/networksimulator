import threading

from application import testapp
from network import unreliable
from transport import reliable

NUM_PACKETS = 1000
ERROR_PROBABILITY = 0.5
LOSS_PROBABILITY = 0.5

ADDR_A = ('127.0.0.1', 5555)
ADDR_B = ('127.0.0.1', 6666)

if __name__ == '__main__':
    udt_a = unreliable.UnreliableDataTransfer(ADDR_A, ADDR_B, LOSS_PROBABILITY, ERROR_PROBABILITY)
    rdt_a = reliable.ReliableDataTransfer(udt_a)
    app_a = testapp.SingleDirectionTestApp(rdt_a, NUM_PACKETS, "A")

    udt_b = unreliable.UnreliableDataTransfer(ADDR_B, ADDR_A, LOSS_PROBABILITY, ERROR_PROBABILITY)
    rdt_b = reliable.ReliableDataTransfer(udt_b)
    app_b = testapp.SingleDirectionTestApp(rdt_b, NUM_PACKETS, "B")

    sender = threading.Thread(name='sender', target=app_a.send_data, daemon=True)
    receiver = threading.Thread(name='receiver', target=app_b.receive_data, daemon=True)
    receiver.start()
    sender.start()
    receiver.join()
    sender.join()
