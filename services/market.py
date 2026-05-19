import random
import math

STOCKS = {
    'TSLA': {'name': 'Tesla Inc.', 'base': 350.0, 'vol': 0.03},
    'SPCE': {'name': 'SpaceX Corp.', 'base': 180.0, 'vol': 0.04},
    'NLNK': {'name': 'Neuralink Corp.', 'base': 75.0, 'vol': 0.05},
    'XCOM': {'name': 'X Holdings', 'base': 45.0, 'vol': 0.06},
    'BRNG': {'name': 'Boring Co.', 'base': 25.0, 'vol': 0.07},
}

price_cache = {}

def get_initial_prices():
    prices = {}
    for sym, data in STOCKS.items():
        prices[sym] = round(data['base'] * random.uniform(0.95, 1.05), 2)
    return prices

def update_prices(prices):
    for sym, data in STOCKS.items():
        change = data['vol'] * random.gauss(0, 1)
        prices[sym] = round(prices[sym] * (1 + change), 2)
        prices[sym] = max(prices[sym], data['base'] * 0.5)
    return prices

def generate_history(symbol, points=30):
    data = STOCKS.get(symbol)
    if not data:
        return []
    price = data['base']
    history = []
    for i in range(points):
        change = data['vol'] * random.gauss(0, 1)
        price = round(price * (1 + change), 2)
        price = max(price, data['base'] * 0.5)
        history.append(price)
    return history

def get_all_prices():
    if 'prices' not in price_cache:
        price_cache['prices'] = get_initial_prices()
    else:
        price_cache['prices'] = update_prices(price_cache['prices'])
    return price_cache['prices']

def get_stock_info():
    result = []
    prices = get_all_prices()
    for sym, data in STOCKS.items():
        change = round((prices[sym] - data['base']) / data['base'] * 100, 2)
        result.append({
            'symbol': sym,
            'name': data['name'],
            'price': prices[sym],
            'change': change,
            'change_str': f'+{change}%' if change >= 0 else f'{change}%',
            'positive': change >= 0
        })
    return result
