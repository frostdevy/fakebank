from flask import Flask, render_template, jsonify, request, session
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Fake database (w pamięci – dla Vercel działa)
balances = {}  # session_id -> balance

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/balance', methods=['GET'])
def get_balance():
    session_id = session.get('id', 'default')
    if session_id not in balances:
        balances[session_id] = 0.00
    return jsonify({'balance': balances[session_id]})

@app.route('/api/balance', methods=['POST'])
def set_balance():
    session_id = session.get('id', 'default')
    data = request.json
    new_balance = float(data.get('balance', 0))
    balances[session_id] = new_balance
    return jsonify({'balance': new_balance, 'success': True})

@app.route('/api/tokens', methods=['GET'])
def get_tokens():
    # Symulacja danych tokenów
    return jsonify({
        'tokens': [
            {'name': 'ARX', 'value': 1.23},
            {'name': 'QUQ', 'value': 492.45},
            {'name': 'BTC', 'value': 10004}
        ],
        'meme_coins': [
            {'name': 'Fartcoin', 'change': 0.14}
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
