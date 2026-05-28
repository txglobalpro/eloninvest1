import requests
import time
from flask import current_app

USDT_TRC20_CONTRACT = 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t'

class CryptoVerifier:
    @staticmethod
    def verify_trc20_txid(txid, expected_to_address, expected_amount):
        expected_to = expected_to_address.lower()
        try:
            resp = requests.get(
                f'https://api.trongrid.io/v1/transactions/{txid}/events',
                params={'only_confirmed': 'true'},
                timeout=15
            )
            if resp.status_code != 200:
                return {'valid': False, 'error': f'API error: {resp.status_code}'}
            data = resp.json()
            if not data.get('success') or not data.get('data'):
                return {'valid': False, 'error': 'Transaction not found or not confirmed'}
            for event in data['data']:
                if event.get('contract_address', '').lower() != USDT_TRC20_CONTRACT.lower():
                    continue
                if event.get('event_name') != 'Transfer':
                    continue
                result = event.get('result', {})
                to_addr = result.get('to', '').lower()
                if to_addr != expected_to:
                    continue
                value_raw = int(result.get('value', 0))
                value = value_raw / 1_000_000
                if abs(value - expected_amount) > 0.01:
                    continue
                from_addr = result.get('from', '')
                return {'valid': True, 'from': from_addr, 'to': to_addr, 'value': value}
            return {'valid': False, 'error': 'No matching Transfer event found for this address and amount'}
        except requests.exceptions.Timeout:
            return {'valid': False, 'error': 'Blockchain API timeout. Try again.'}
        except Exception as e:
            return {'valid': False, 'error': str(e)}

    @staticmethod
    def verify_txid(txid, network, wallet_address, amount):
        network = network.upper().replace('-', '')
        if network == 'TRC20':
            return CryptoVerifier.verify_trc20_txid(txid, wallet_address, amount)
        return {'valid': False, 'error': f'Network {network} verification not yet supported'}
