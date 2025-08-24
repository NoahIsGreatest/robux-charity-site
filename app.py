# app.py
from flask import Flask, render_template, request, jsonify
import csv
import os
from datetime import datetime
import requests

app = Flask(__name__)

CSV_FILE = 'requests.csv'

# Initialize CSV if not exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['username', 'type', 'amount', 'timestamp'])

def get_total_credits(username):
    total = 0.0
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['username'] == username:
                    if row['type'] == 'earn':
                        total += float(row['amount'])
                    elif row['type'] == 'withdraw':
                        total -= float(row['amount'])
    return total

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_avatar', methods=['POST'])
def get_avatar():
    data = request.json
    username = data.get('username')
    if username:
        # Get user ID from username
        api_response = requests.post('https://users.roblox.com/v1/usernames/users', json={"usernames": [username], "excludeBannedUsers": True})
        if api_response.status_code == 200:
            user_data = api_response.json()
            if user_data.get('data') and len(user_data['data']) > 0:
                user_id = user_data['data'][0]['id']
                # Get avatar headshot
                avatar_response = requests.get(f'https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=150x150&format=Png&isCircular=false')
                if avatar_response.status_code == 200:
                    avatar_data = avatar_response.json()
                    if avatar_data.get('data') and len(avatar_data['data']) > 0:
                        avatar_url = avatar_data['data'][0]['imageUrl']
                        return jsonify({'avatar_url': avatar_url})
    return jsonify({'error': 'User not found'}), 404

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
        amount = 0.5
        timestamp = datetime.now().isoformat()
        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([username, 'earn', amount, timestamp])
        total_credits = get_total_credits(username)
        return jsonify({'credits': total_credits})
    return jsonify({'error': 'No username provided'}), 400

@app.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.json
    username = data.get('username')
    amount = data.get('amount')
    if username and amount > 0:
        total = get_total_credits(username)
        if total >= amount:
            timestamp = datetime.now().isoformat()
            with open(CSV_FILE, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([username, 'withdraw', amount, timestamp])
            new_total = get_total_credits(username)
            return jsonify({'credits': new_total})
        else:
            return jsonify({'error': 'Insufficient credits'}), 400
    return jsonify({'error': 'Invalid request'}), 400

if __name__ == '__main__':
    app.run(debug=True)
