from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

from model.stock.calculator import Calculator

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('menu.html')


@app.route('/stock_odds_menu')
def stock_odds_menu():
    return render_template('stock_odds_menu.html')


@app.route('/query_recommended_stock_page')
def query_recommended_stock_page():
    return render_template('query_recommended_stock_page.html')


@app.route('/read_recommend_stock_odds', methods=['GET', 'POST'])
def read_recommend_stock_odds():
    days = request.form.get('days_dropdown')
    odds = request.form.get('odds_dropdown')
    odds = float(odds) / 10
    calculator = create_calculator()
    recommended_stock_list = calculator.read_recommended_stock(days, odds)
    return render_template('query_recommended_stock_page.html', recommended_stock_list=recommended_stock_list)


def create_calculator():
    return Calculator()


if __name__ == '__main__':
    # app.run()
    app.run(debug=True, port=5000)  # 存檔自動更新網頁
