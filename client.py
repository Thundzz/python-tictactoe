import socket
import threading
import time
import random
import string


def build_header(header_size, length):
    h =  str(length).rjust(64, " ")
    return h

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost",9000))

header_size = 64

while True:
    length = random.randint(5, 10)
    msg = "".join(random.sample(string.ascii_letters, length))
    header = build_header(header_size, length)
    client.send(header.encode("ascii"))
    client.send(msg.encode("ascii"))
    # time.sleep(0.1)