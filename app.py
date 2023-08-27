from flask import Flask, request, jsonify
import json
import re

app = Flask(__name__)

def get_exchange_rate(source_currency, target_currency):
    with open('exchange_rate.json', 'r') as f:
        exchange_rates = json.load(f)
    return exchange_rates['currencies'][source_currency][target_currency]

@app.route('/hello', methods=['GET'])
def exchange():
    return jsonify(message='Hello world')

@app.route('/api/v1/exchange', methods=['GET'])
def convert_currency():
    source_currency = request.args.get('source')
    target_currency = request.args.get('target')
    amount_str = request.args.get('amount').replace(',', '')
    is_round = request.args.get('round', True)

    amount_match = re.search(r'([\d.]+)', amount_str)
    if amount_match:
        amount = float(amount_match.group(1))
    else:
        return jsonify({'error': 'FormatError: Invalid amount format'})

    exchange_rate = get_exchange_rate(source_currency, target_currency)
    converted_amount = amount * exchange_rate

    converted_rounded = round(converted_amount, 2) if is_round else converted_amount
    converted_formatted = format(converted_rounded, ',.2f')

    result = {
        'source': source_currency,
        'target': target_currency,
        'exchange_rate': exchange_rate,
        'amount': amount,
        'converted_amount': converted_formatted
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
