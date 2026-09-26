import json
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .engine import epsilon_greedy, ucb1

BASE_DIR = Path(__file__).resolve().parents[1]
WEB_DIR = BASE_DIR / "web"


def _parse_arms(value):
    if isinstance(value, list):
        return [float(x) for x in value]
    if isinstance(value, str):
        return [float(x.strip()) for x in value.split(",") if x.strip()]
    return []


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def log_message(self, format, *args):
        return

    def _send_json(self, payload, status=HTTPStatus.OK):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        if not length:
            return {}
        body = self.rfile.read(length)
        return json.loads(body.decode("utf-8"))

    def do_POST(self):
        if self.path == "/api/simulate":
            payload = self._read_json()
            arms = _parse_arms(payload.get("arms", []))
            rounds = int(payload.get("rounds", 200))
            epsilon = float(payload.get("epsilon", 0.1))
            self._send_json(epsilon_greedy(arms, rounds=rounds, epsilon=epsilon))
            return
        if self.path == "/api/ucb":
            payload = self._read_json()
            arms = _parse_arms(payload.get("arms", []))
            rounds = int(payload.get("rounds", 200))
            self._send_json(ucb1(arms, rounds=rounds))
            return
        self._send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)

    def do_GET(self):
        if self.path.startswith("/api/"):
            self._send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)
            return
        super().do_GET()


def run(host="127.0.0.1", port=5173):
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Multi Armed Bandit Simulator running at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run Multi Armed Bandit Simulator")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5173)
    args = parser.parse_args()

    run(host=args.host, port=args.port)
