from flask import Flask, request, jsonify, send_from_directory
import json
import time
import os

app = Flask(__name__)

USERS_FILE = 'users.json'

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def style():
    return send_from_directory('.', 'style.css')

@app.route('/watch_ad', methods=['POST'])
def watch_ad():
    username = request.json.get('username')
    users = load_users()
    if username not in users:
        users[username] = {'credits': 0, 'last_withdraw': 0, 'ads_watched': 0}

    users[username]['credits'] += 0.5
    users[username]['ads_watched'] += 1
    save_users(users)
    return jsonify({'credits': users[username]['credits'], 'ads_watched': users[username]['ads_watched']})

@app.route('/withdraw', methods=['POST'])
def withdraw():
    username = request.json.get('username')
    amount = float(request.json.get('amount'))
    users = load_users()

    if username not in users:
        return jsonify({'error': 'User not found'}), 400

    user = users[username]
    now = time.time()

    # 3-day cooldown = 259200 seconds
    if now - user['last_withdraw'] < 259200:
        remaining = 259200 - (now - user['last_withdraw'])
        return jsonify({'error': f'Wait {int(remaining//3600)}h before next withdrawal'}), 400

    if amount > user['credits']:
        return jsonify({'error': 'Not enough credits'}), 400

    if amount > 80:
        amount = 80

    user['credits'] -= amount
    user['last_withdraw'] = now
    save_users(users)
    return jsonify({'success': f'Withdraw request of {amount} Robux submitted. Wait up to 1 week.', 'credits': user['credits']})

if __name__ == '__main__':
    app.run(debug=True)
