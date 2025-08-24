import csv
import os
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, session, send_from_directory, render_template


APP_SECRET = os.environ.get("APP_SECRET", "change-me-please")
CSV_PATH = os.environ.get("CSV_PATH", "requests.csv")
CREDIT_INCREMENT = 0.5
WITHDRAW_MIN = 7
WITHDRAW_MAX = 80
WITHDRAW_COOLDOWN_DAYS = 3


app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = APP_SECRET


# Ensure CSV has a header
CSV_HEADER = [
"timestamp", "username", "action", "amount", "balance", "note"
]


def ensure_csv():
if not os.path.exists(CSV_PATH):
with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
writer = csv.writer(f)
writer.writerow(CSV_HEADER)




def append_row(username: str, action: str, amount: float | None, balance: float | None, note: str = ""):
ensure_csv()
with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
writer = csv.writer(f)
writer.writerow([
datetime.utcnow().isoformat(), username, action,
("" if amount is None else f"{amount:.2f}"),
("" if balance is None else f"{balance:.2f}"), note
])




def get_user_events(username: str):
ensure_csv()
events = []
if not os.path.exists(CSV_PATH):
return events
with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
reader = csv.DictReader(f)
for row in reader:
if row.get("username") == username:
events.append(row)
return events




def current_balance(username: str) -> float:
events = get_user_events(username)
# Balance is derived from the last non-empty balance field; if missing, recompute
last_with_balance = None
for row in events:
if row.get("balance"):
last_with_balance = float(row["balance"]) # keep updating
if last_with_balance is not None:
return last_with_balance


# Fallback recompute from actions
bal = 0.0
for row in events:
action = row.get("action", "")
if action == "credit":
bal += float(row.get("amount") or 0)
elif action == "withdraw":
bal -= float(row.get("amount") or 0)
app.run(host="0.0.0.0", port=port, debug=True)
