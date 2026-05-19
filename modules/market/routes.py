from flask import Blueprint, render_template, jsonify
from services.market import get_stock_info, generate_history

market_bp = Blueprint('market', __name__, template_folder='../../templates/market')

@market_bp.route('/')
def index():
    stocks = get_stock_info()
    return render_template('market/index.html', stocks=stocks)

@market_bp.route('/data/<symbol>')
def data(symbol):
    history = generate_history(symbol)
    return jsonify(history)
