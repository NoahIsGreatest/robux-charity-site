from flask import Flask, render_template, request, redirect, url_for, jsonify
import csv
import os
from datetime import datetime, timedelta

app = Flask(__name__)

USERS_FILE = "requests.csv"

# --- Helper functions ---
def read_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                users[row["username"]] = row
    return users

def save_users(users):
    with open(USERS_FILE, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["username", "balance", "last_withdraw_date", "withdraw_requests"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in users.values():
            writer.writerow(user)

# --- Routes ---
@app.route("/")
def home():
    return render_template("index.html", username=None)

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username").strip()
    if not username:
        return redirect(url_for("home"))
    users = read_users()
    if username not in users:
        users[username] = {
            "username": username,
            "balance": "0",
            "last_withdraw_date": "",
            "withdraw_requests": ""
        }
        save_users(users)
    return redirect(url_for("dashboard", username=username))

@app.route("/dashboard/<username>")
def dashboard(username):
    users = read_users()
    if username not in users:
        return redirect(url_for("home"))
    user = users[username]
    return render_template("index.html", username=username, balance=user["balance"])

@app.route("/watch_ad", methods=["POST"])
def watch_ad():
    data = request.get_json()
    username = data.get("username")
    if not username:
        return jsonify({"error": "User not found"})
    users = read_users()
    if username not in users:
        return jsonify({"error": "User not found"})
    # Add 0.5 credits
    balance = float(users[username]["balance"]) + 0.5
    users[username]["balance"] = str(balance)
    save_users(users)
    return jsonify({"balance": balance})

@app.route("/withdraw", methods=["POST"])
def withdraw():
    data = request.get_json()
    username = data.get("username")
    amount = float(data.get("amount", 0))
    users = read_users()
    if username not in users:
        return jsonify({"error": "User not found"})
    user = users[username]

    # Withdraw cooldown 3 days
    last_date_str = user.get("last_withdraw_date", "")
    if last_date_str:
        last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
        if datetime.now() < last_date + timedelta(days=3):
            return jsonify({"error": "You can only withdraw every 3 days."})

    # Check amount limits
    if amount < 7 or amount > 80:
        return jsonify({"error": "Withdrawal must be between 7 and 80 credits."})

    if float(user["balance"]) < amount:
        return jsonify({"error": "Insufficient balance."})

    # Update balance and last withdraw
    user["balance"] = str(float(user["balance"]) - amount)
    user["last_withdraw_date"] = datetime.now().strftime("%Y-%m-%d")
    if user["withdraw_requests"]:
        user["withdraw_requests"] += f";{amount}-{datetime.now().strftime('%Y-%m-%d')}"
    else:
        user["withdraw_requests"] = f"{amount}-{datetime.now().strftime('%Y-%m-%d')}"
    save_users(users)
    return jsonify({"success": f"Withdraw request of {amount} submitted! It may take up to 1 week.", "balance": user["balance"]})

if __name__ == "__main__":
    app.run(debug=True)
