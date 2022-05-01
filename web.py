from json import dump

from flask import Flask, render_template, request, json, jsonify
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
    return render_template('query_recommended_stock_page.html', recommended_stock_list='')


@app.route('/read_recommended_stock', methods=['POST'])
def read_recommended_stock():
    days = request.form.get('days_dropdown')
    odds = request.form.get('odds_dropdown')
    odds = float(odds) / 10
    recommended_stock_list = premium_member.read_recommended_stock(days, odds)
    data = list()
    for i in range(len(recommended_stock_list)):
        d = dict()
        d['id'] = i+1
        d['content'] = recommended_stock_list[i]
        data.append(d)
    return render_template('query_recommended_stock_page.html', recommended_stock_list=data)


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
