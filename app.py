from flask import Flask, request, jsonify, send_from_directory
import csv

app = Flask(__name__)
CSV_FILE = 'requests.csv'

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Save Robux withdraw request
@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    username = data.get('username')
    robux_amount = data.get('robux_amount')
    credits_used = data.get('credits_used')
    if not username or not robux_amount or not credits_used:
        return jsonify({'success': False})

    try:
        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([username, robux_amount, credits_used])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    
if __name__ == '__main__':
    app.run(debug=True)
