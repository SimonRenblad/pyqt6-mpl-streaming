import socketserver
import random
import time

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            while True:
                self.request.sendall(str(random.randint(0, 10)).encode() + b"\n")
                time.sleep(0.2)
        except (BrokenPipeError, ConnectionResetError):
            pass

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
