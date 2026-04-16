import json
from pathlib import Path
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import error, parse, request

HOST = "127.0.0.1"
PORT = 5000
BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "index.html"


class TranslatorHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.end_headers()

    def do_GET(self):
        if self.path in ["/", "/index.html"]:
            if not INDEX_FILE.exists():
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "index.html not found."}).encode("utf-8"))
                return

            self._set_headers(200, "text/html; charset=utf-8")
            self.wfile.write(INDEX_FILE.read_bytes())
            return

        if self.path in ["/translate", "/api/translate"]:
            self._set_headers(405)
            self.wfile.write(
                json.dumps({"error": "Use POST /api/translate with a JSON body."}).encode("utf-8")
            )
            return

        self._set_headers(404)
        self.wfile.write(json.dumps({"error": "Route not found."}).encode("utf-8"))

    def do_OPTIONS(self):
        self._set_headers(204)

    def do_POST(self):
        if self.path not in ["/translate", "/api/translate"]:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Route not found."}).encode("utf-8"))
            return

        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length)

        try:
            body = json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid JSON body."}).encode("utf-8"))
            return

        endpoint = (body.get("endpoint") or "").strip().rstrip("/")
        key = (body.get("key") or "").strip()
        region = (body.get("region") or "").strip()
        text = (body.get("text") or "").strip()
        targets = body.get("targets") or []

        if not endpoint or not key or not text or not isinstance(targets, list) or not targets:
            self._set_headers(400)
            self.wfile.write(
                json.dumps({"error": "endpoint, key, text, and targets are required."}).encode("utf-8")
            )
            return

        params = [("api-version", "3.0")]
        for language in targets:
            params.append(("to", str(language)))

        translator_url = f"{endpoint}/translate?{parse.urlencode(params)}"
        azure_body = json.dumps([{"text": text}]).encode("utf-8")

        azure_headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": key,
            "X-ClientTraceId": str(uuid.uuid4()),
        }
        if region:
            azure_headers["Ocp-Apim-Subscription-Region"] = region

        req = request.Request(
            translator_url,
            data=azure_body,
            headers=azure_headers,
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=25) as response:
                response_payload = json.loads(response.read().decode("utf-8"))
        except error.HTTPError as http_err:
            details = http_err.read().decode("utf-8", errors="ignore")
            self._set_headers(http_err.code)
            self.wfile.write(json.dumps({"error": details or str(http_err)}).encode("utf-8"))
            return
        except error.URLError as url_err:
            self._set_headers(502)
            self.wfile.write(json.dumps({"error": f"Unable to reach Azure endpoint: {url_err.reason}"}).encode("utf-8"))
            return
        except Exception as exc:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(exc)}).encode("utf-8"))
            return

        translations = {}
        try:
            items = response_payload[0].get("translations", [])
            for item in items:
                lang_code = item.get("to")
                translated_text = item.get("text")
                if lang_code:
                    translations[lang_code] = translated_text
        except (IndexError, AttributeError, TypeError):
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": "Unexpected Azure response shape."}).encode("utf-8"))
            return

        self._set_headers(200)
        self.wfile.write(json.dumps({"translations": translations}).encode("utf-8"))


def run_server():
    server = HTTPServer((HOST, PORT), TranslatorHandler)
    print(f"Backend running at http://{HOST}:{PORT}")
    print(f"Open http://{HOST}:{PORT} in your browser")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
