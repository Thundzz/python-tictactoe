import socket
import threading
import time


class ClientHandler:
    def __init__(self):
        self.state = "HEADER"
        self.header_size = 64
        self.data = []
        self.messages = []
        self.conn = None
        self.running = True

    def run(self, conn, addr):
        self.conn = conn
        while self.running:
            # print(f"Received {len(self.data)} bytes from client")
            dt = conn.recv(4096)
            self.data.extend(list(dt))
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

class ServerListener:
    def __init__(self):
        self.client_handler = None
        self.client_thread = None

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("0.0.0.0",9000))
        self.socket.listen(1)
        print("Listening to incoming ")
        conn, addr = self.socket.accept()
        self.client_handler = ClientHandler()
        thread = threading.Thread(target=self.client_handler.run, args=(conn, addr))
        self.client_thread = thread
        thread.start()
        # self.socket.close()

    def get_messages(self):
        messages = []
        while self.client_handler.messages:
            messages.append(self.client_handler.messages.pop(0))

        return messages

    def stop(self):
        if self.client_handler:
            self.client_handler.stop()

        if self.client_thread:
            self.client_thread.join()

        if self.socket:
            self.socket.close()

if __name__ == '__main__':
    try:
        server = ServerListener()
        server.start()

        while True:
            # print("Polling messages")
            msgs = server.get_messages()
            if msgs:
                print(msgs)
            time.sleep(0.5)
            # print(msg)
    finally:
        server.stop()
        print("cleanup")