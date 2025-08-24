from flask import Flask, request, jsonify, render_template
import csv, os, time

app = Flask(__name__)

CSV_FILE = "requests.csv"

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/save", methods=["POST"])
def save():
    data = request.json
    username = data["username"]
    balance = data["balance"]
    ads = data["adsWatched"]

    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["username", "balance", "adsWatched", "lastWithdraw"])
        writer.writerow([username, balance, ads, "0"])
    return jsonify({"status": "saved"})

@app.route("/withdraw", methods=["POST"])
def withdraw():
    username = request.json["username"]
    rows = []
    allowed = False
    message = "User not found."

    if os.path.isfile(CSV_FILE):
        with open(CSV_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["username"] == username:
                    last = float(row["lastWithdraw"])
                    now = time.time()
                    if now - last >= 3*24*3600:  # 3 days
                        row["lastWithdraw"] = str(now)
                        message = "✅ Withdrawal successful! Wait 3 days before next one."
                        allowed = True
                    else:
                        remaining = int((3*24*3600 - (now-last)) / 3600)
                        message = f"⏳ You must wait {remaining} hours before next withdrawal."
                rows.append(row)

        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["username","balance","adsWatched","lastWithdraw"])
            writer.writeheader()
            writer.writerows(rows)

    return jsonify({"message": message})

if __name__ == "__main__":
    app.run(debug=True)
