from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap

from model.member.premium_member import PremiumMember

app = Flask(__name__)
bootstrap = Bootstrap(app)
premium_member = PremiumMember('t109598087@ntut.org.tw', 'islab')


@app.route('/')
def index():
    return render_template('menu.html')


@app.route('/stock_odds_menu')
def stock_odds_menu():
    return render_template('stock_odds_menu.html')


@app.route('/query_recommended_stock_page')
def query_recommended_stock_page():
    return render_template('query_recommended_stock_page.html')


@app.route('/read_recommended_stock', methods=['GET', 'POST'])
def read_recommended_stock():
    days = int(request.values.get('days_dropdown'))
    odds = int(request.values.get('odds_dropdown'))
    limit = request.values.get('limit', 10)
    offset = request.values.get('offset', 1)
    odds = int(odds) / 10
    # recommended_stock_list = premium_member.read_recommended_stock(days, odds)
    recommended_stock_list = [{'stock_id': 8080, 'stock_name': '永利聯合', 'rsi_6': 100.0, 'odds': 0.93},
                              {'stock_id': 8477, 'stock_name': '創業家', 'rsi_6': 75.61, 'odds': 0.89},
                              {'stock_id': 4712, 'stock_name': '南璋', 'rsi_6': 60.71, 'odds': 0.93},
                              {'stock_id': 9802, 'stock_name': '鈺齊-KY', 'rsi_6': 92.0, 'odds': 0.93}]
    for i in range(20):
        recommended_stock_list.append(recommended_stock_list[i % 4])
    json_data = jsonify({'total': len(recommended_stock_list), 'rows': recommended_stock_list[int(offset):(int(offset) + int(limit))]})
    return json_data


@app.route('/query_specific_stock_page')
def query_specific_stock_page():
    return render_template('query_specific_stock_page.html')


@app.route('/read_stock_odds', methods=['GET', 'POST'])
def read_stock_odds():
    stock_id = request.form.get('stock_id')
    stock_id = int(stock_id)
    stock_odds_list = premium_member.read_stock_odds(stock_id)
    return render_template('query_specific_stock_page.html', stock_odds_list=stock_odds_list)


if __name__ == '__main__':
    # app.run()
    app.run(debug=True, port=5000)  # 存檔自動更新網頁
