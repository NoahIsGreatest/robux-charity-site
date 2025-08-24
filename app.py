# app.py
from flask import Flask, render_template, request, jsonify
import csv
import os
from datetime import datetime

app = Flask(__name__)

CSV_FILE = 'requests.csv'

# Initialize CSV if not exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['username', 'credits_earned', 'timestamp'])

def get_total_credits(username):
    total = 0.0
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['username'] == username:
                    total += float(row['credits_earned'])
    return total

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_credits', methods=['POST'])
def get_credits():
    data = request.json
    username = data.get('username')
    if username:
        total_credits = get_total_credits(username)
        return jsonify({'credits': total_credits})
    return jsonify({'error': 'No username provided'}), 400

@app.route('/watch_ad', methods=['POST'])
def watch_ad():
    data = request.json
    username = data.get('username')
    if username:
        credits_earned = 0.5
        timestamp = datetime.now().isoformat()
        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([username, credits_earned, timestamp])
        total_credits = get_total_credits(username)
        return jsonify({'credits': total_credits})
    return jsonify({'error': 'No username provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)
