#!/usr/bin/env python3
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

HOST = "localhost"
PORT = 5000

OPERATIONS = {
    "/add": ("addition", lambda a, b: a + b),
    "/subtract": ("subtraction", lambda a, b: a - b),
    "/multiply": ("multiplication", lambda a, b: a * b),
    "/divide": ("division", lambda a, b: a / b),
}

class CalculatorHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code, payload):
        body = json.dumps(payload, indent=4).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        params = parse_qs(parsed.query)

        if path not in OPERATIONS:
            self._send_json(404, {
                "error": "Unknown endpoint",
                "available_endpoints": list(OPERATIONS.keys()),
            })
            return

        operation_name, func = OPERATIONS[path]

        if "a" not in params or "b" not in params:
            self._send_json(400, {
                "error": "Missing query parameters. Provide both 'a' and 'b'.",
                "example": f"http://{HOST}:{PORT}{path}?a=5&b=3",
            })
            return

        try:
            a = float(params["a"][0])
            b = float(params["b"][0])
        except ValueError:
            self._send_json(400, {
                "error": "Parameters 'a' and 'b' must be numbers.",
            })
            return

        if path == "/divide" and b == 0:
            self._send_json(400, {
                "error": "Division by zero is not allowed.",
            })
            return

        result = func(a, b)

        a = int(a) if a.is_integer() else a
        b = int(b) if b.is_integer() else b
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        self._send_json(200, {
            "a": a,
            "b": b,
            "operation": operation_name,
            "result": result,
        })

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} - {fmt % args}")


def main():
    server = HTTPServer((HOST, PORT), CalculatorHandler)
    print(f"Server running at http://{HOST}:{PORT}")
    print("Endpoints: /add, /subtract, /multiply, /divide")
    print(f"Try: http://{HOST}:{PORT}/add?a=5&b=3")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        server.server_close()


if __name__ == "__main__":
    main()
