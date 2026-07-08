from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading
from PyQt6.QtCore import QObject, pyqtSignal


class BridgeSignal(QObject):
    message = pyqtSignal(str)


class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True


class BridgeServer:
    def __init__(self, assistant, port=8769):
        self.assistant = assistant
        self.port = port

        self.signal = BridgeSignal()
        self.signal.message.connect(self.assistant.set_speech)

        server_ref = self

        class Handler(BaseHTTPRequestHandler):

            # -------------------------
            # CORS HEADERS (IMPORTANT)
            # -------------------------
            def send_cors(self):
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")

            # -------------------------
            # Preflight request (CORS)
            # -------------------------
            def do_OPTIONS(self):
                self.send_response(200)
                self.send_cors()
                self.end_headers()

            # -------------------------
            # Actual POST request
            # -------------------------
            def do_POST(self):
                length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(length)

                try:
                    data = json.loads(body.decode("utf-8"))
                    msg = data.get("message", "")

                    server_ref.signal.message.emit(msg)

                    self.send_response(200)
                    self.send_cors()
                    self.end_headers()
                    self.wfile.write(b"OK")

                except Exception as e:
                    self.send_response(500)
                    self.send_cors()
                    self.end_headers()
                    self.wfile.write(str(e).encode())

        self.server = ReusableHTTPServer(("127.0.0.1", port), Handler)

    def start(self):
        thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        thread.start()