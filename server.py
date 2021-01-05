import socket
import threading
import time


class ConnectionHandler:
    def __init__(self):
        self.state = "HEADER"
        self.header_size = 64
        self.data = []
        self.messages = []
        self.conn = None
        self.running = True

    def run(self, conn):
        self.conn = conn
        while self.running:
            # print(f"Received {len(self.data)} bytes from client")
            dt = conn.recv(4096)
            self.data.extend(list(dt))
            """
            This is very ugly, but basically, we need to continue decoding while we are making progress.
            Looping a bunch of time should do in most cases >___<'
            """
            for i in range(100):
                if len(self.data) >= self.header_size and self.state == "HEADER":
                    self.current_data_size = int(bytes(self.data[:self.header_size]).decode("ascii"))
                    self.data = self.data[self.header_size:]
                    self.state = "DATA"

                if self.state == "DATA" and len(self.data) >= self.current_data_size:
                    msg = bytes(self.data[:self.current_data_size]).decode("ascii")
                    self.messages.append(msg)
                    self.data = self.data[self.current_data_size:]
                    self.current_data_size = None
                    self.state = "HEADER"

    def stop(self):
        self.running = False
        if self.conn:
            self.conn.close()

    def send_messages(self, messages):
        for msg in messages:
            encoded = msg.encode("ascii")
            length = len(encoded)
            header = self.build_header(self.header_size, length)
            self.conn.sendall(header.encode("ascii"))
            self.conn.sendall(encoded)

    @staticmethod
    def build_header(header_size, length):
        return str(length).rjust(64, " ")

class Server:
    def __init__(self):
        self.connection_handler = None
        self.connection_thread = None

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("0.0.0.0",9000))
        self.socket.listen(1)
        print("Listening to incoming ")
        conn, addr = self.socket.accept()
        self.connection_handler = ConnectionHandler()
        thread = threading.Thread(target=self.connection_handler.run, args=[conn])
        self.connection_thread = thread
        thread.start()
        # self.socket.close()

    def get_messages(self):
        messages = []
        while self.connection_handler.messages:
            messages.append(self.connection_handler.messages.pop(0))

        return messages

    def stop(self):
        if self.connection_handler:
            self.connection_handler.stop()

        if self.connection_thread:
            self.connection_thread.join()

        if self.socket:
            self.socket.close()

class Client:
    def __init__(self, server_ip, port=9000):
        self.server_ip = server_ip
        self.port = port

    def start(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((self.server_ip, self.port))
        self.connection_handler = ConnectionHandler()
        thread = threading.Thread(target=self.connection_handler.run, args=[conn])
        self.connection_thread = thread
        thread.start()

    def send_messages(self, msgs):
        self.connection_handler.send_messages(msgs)

    def stop(self):
        if self.conn:
            self.conn.close()

if __name__ == '__main__':
    try:
        server = Server()
        server.start()
        while True:
            # print("Polling messages")
            msgs = server.get_messages()
            print("hi")
            if msgs:
                print(msgs)
            time.sleep(0.5)
            # print(msg)
    finally:
        server.stop()
        print("cleanup")