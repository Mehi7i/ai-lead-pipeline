import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
url = f"https://api.telegram.org/bot{token}/sendMessage"
r = requests.post(url, json={"chat_id": chat_id, "text": "Lead pipeline test: Telegram is connected."})
print(r.status_code)
print(r.text)