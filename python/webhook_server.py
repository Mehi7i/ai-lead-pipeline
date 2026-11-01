import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests
from dotenv import load_dotenv

from crm_writer import save_lead
from qualify_lead import qualify

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def notify(lead, result, lead_id):
    text = (
        f"New lead #{lead_id}\n"
        f"Name: {lead.get('name')}\n"
        f"Score: {result.get('score')} ({result.get('source')})\n"
        f"Reason: {result.get('reason')}\n"
        f"Message: {lead.get('message')}"
    )
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text},
        timeout=20,
    )


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        page = """<!doctype html>
<html>
<head><meta charset="utf-8"><title>New lead</title></head>
<body>
  <h1>Send a lead</h1>
  <form id="f">
    <p>Name <input name="name" required></p>
    <p>Email <input name="email" type="email" required></p>
    <p>Budget <input name="budget"></p>
    <p>Message <textarea name="message" required></textarea></p>
    <p>Secret <input name="secret" required></p>
    <button>Send</button>
  </form>
  <pre id="out"></pre>
  <script>
    document.getElementById("f").onsubmit = async (e) => {
      e.preventDefault();
      const data = Object.fromEntries(new FormData(e.target));
      const secret = data.secret;
      delete data.secret;
      const res = await fetch("/lead", {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-Webhook-Secret": secret},
        body: JSON.stringify(data)
      });
      document.getElementById("out").textContent = await res.text();
    };
  </script>
</body>
</html>"""
        body = page.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        secret = self.headers.get("X-Webhook-Secret", "")
        if secret != os.getenv("WEBHOOK_SECRET", ""):
               self.send_response(401)
               self.end_headers()
               return
        length = int(self.headers.get("Content-Length", 0))
        lead = json.loads(self.rfile.read(length) or b"{}")
        result = qualify(lead)
        lead_id = save_lead(lead, result)
        notify(lead, result, lead_id)
        body = json.dumps({"ok": True, "lead_id": lead_id, **result}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print("Listening on http://127.0.0.1:8787/lead")
    HTTPServer(("127.0.0.1", 8787), Handler).serve_forever()