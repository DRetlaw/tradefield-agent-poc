import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from http.server import BaseHTTPRequestHandler
import json
from src.agent import TradeFieldAgent

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("content-length", "0"))
        body = json.loads(self.rfile.read(length) or "{}")
        request = body.get("request", "")
        approved = bool(body.get("approved", False))
        try:
            result = TradeFieldAgent().run(request, approved=approved)
            payload = result
            status = 200
        except Exception as exc:
            payload = {"error": str(exc)}
            status = 500
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok", "service": "tradefield-agent"}).encode())
