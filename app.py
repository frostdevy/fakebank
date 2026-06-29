from flask import Flask, render_template, jsonify, request, session
import os
import json

app = Flask(__name__, static_folder='static')
app.secret_key = os.urandom(24)

# Przechowywanie balansów (proste, w pamięci)
balances = {}

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
    data = request.get_json()
    if data and 'balance' in data:
        try:
            new_balance = float(data['balance'])
            if new_balance >= 0:
                balances[session_id] = new_balance
                return jsonify({'balance': new_balance, 'success': True})
        except (ValueError, TypeError):
            pass
    return jsonify({'error': 'Invalid balance'}), 400

@app.route('/api/tokens', methods=['GET'])
def get_tokens():
    return jsonify({
        'tokens': [
            {'name': 'ARX', 'value': 1.23},
            {'name': 'QUQ', 'value': 492.45},
            {'name': 'BTC', 'value': 2000}
        ],
        'meme_coins': [
            {'name': 'Fartcoin', 'change': 0.14}
        ]
    })

# Dla Vercel – handler
def handler(request, context):
    return app(request, context)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
