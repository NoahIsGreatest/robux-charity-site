from flask import Flask, render_template, request, redirect, url_for, jsonify
import csv
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CSV_FILE = "requests.csv"

# Ensure CSV exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "balance", "last_withdraw_date", "withdraw_requests"])

def read_users():
    users = {}
    with open(CSV_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            users[row["username"]] = row
    return users

def save_users(users):
    with open(CSV_FILE, "w", newline="") as f:
        fieldnames = ["username", "balance", "last_withdraw_date", "withdraw_requests"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for u in users.values():
            writer.writerow(u)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username")
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
    username = request.json.get("username")
    users = read_users()
    if username not in users:
        return jsonify({"error": "User not found"})
    balance = float(users[username]["balance"])
    balance += 0.5
    users[username]["balance"] = str(balance)
    save_users(users)
    return jsonify({"balance": balance})

@app.route("/withdraw", methods=["POST"])
def withdraw():
    username = request.json.get("username")
    amount = float(request.json.get("amount", 0))
    users = read_users()
    if username not in users:
        return jsonify({"error": "User not found"})

    user = users[username]
    now = datetime.now()
    last_date_str = user["last_withdraw_date"]
    if last_date_str:
        last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
        if now < last_date + timedelta(days=3):
            return jsonify({"error": "You must wait 3 days between withdrawals"})
    if amount < 7 or amount > 80:
        return jsonify({"error": "Withdrawal amount must be 7-80 credits"})
    balance = float(user["balance"])
    if amount > balance:
        return jsonify({"error": "Not enough balance"})

    user["balance"] = str(balance - amount)
    user["last_withdraw_date"] = now.strftime("%Y-%m-%d")
    if user["withdraw_requests"]:
        user["withdraw_requests"] += f";{amount} on {now.strftime('%Y-%m-%d')}"
    else:
        user["withdraw_requests"] = f"{amount} on {now.strftime('%Y-%m-%d')}"
    save_users(users)
    return jsonify({"success": f"Withdraw request for {amount} credits submitted. It may take up to 1 week to process.", "balance": user["balance"]})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
