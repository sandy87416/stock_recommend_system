from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap

from model.member.member import Member
from model.member.premium_member import PremiumMember

app = Flask(__name__)
bootstrap = Bootstrap(app)
premium_member = PremiumMember('t109598087@ntut.org.tw', 'islab')
member = Member('t109598087@ntut.org.tw', 'islab')


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
    days = int(request.values.get('days'))
    odds = int(request.values.get('odds'))
    limit = request.values.get('limit', 10)
    offset = request.values.get('offset', 1)
    odds = int(odds) / 10
    recommended_stock_list = premium_member.read_recommended_stock(days, odds)
    json_data = jsonify(
        {'total': len(recommended_stock_list), 'rows': recommended_stock_list[int(offset):(int(offset) + int(limit))]})
    return json_data


@app.route('/query_specific_stock_page')
def query_specific_stock_page():
    return render_template('query_specific_stock_page.html')


@app.route('/read_stock_odds', methods=['GET', 'POST'])
def read_stock_odds():
    stock_id = request.values.get('stock_id')
    limit = request.values.get('limit', 10)
    offset = request.values.get('offset', 1)
    stock_id = int(stock_id)
    stock_odds_list = premium_member.read_stock_odds(stock_id)
    json_data = jsonify(
        {'total': len(stock_odds_list), 'rows': stock_odds_list[int(offset):(int(offset) + int(limit))]})
    return json_data


@app.route('/stock_information_menu')
def stock_information_menu():
    return render_template('stock_information_menu.html')


@app.route('/set_stock_id_read_stock_after_hours_information')  # todo: rename
def set_stock_id_read_stock_after_hours_information():
    return render_template('set_stock_id_read_stock_after_hours_information.html')


@app.route('/read_stock_after_hours_information', methods=['GET', 'POST'])
def read_stock_after_hours_information():
    stock_id = request.values.get('stock_id')
    stock_id = int(stock_id)
    stock_after_hours_information = member.read_stock_after_hours_information(stock_id)
    return render_template('read_stock_after_hours_information.html',
                           stock_after_hours_information=stock_after_hours_information)


@app.route('/set_stock_id_read_stock_intraday_information')  # todo: rename
def set_stock_id_read_stock_intraday_information():
    return render_template('set_stock_id_read_stock_intraday_information.html')


@app.route('/read_stock_intraday_information', methods=['GET', 'POST'])
def read_stock_intraday_information():
    stock_id = request.values.get('stock_id')
    stock_id = int(stock_id)
    stock_intraday_information = member.read_stock_intraday_information(stock_id)
    return render_template('read_stock_intraday_information.html',
                           stock_intraday_information=stock_intraday_information)


@app.route('/add_selected_stock')
def add_selected_stock():
    return render_template('add_selected_stock.html')


@app.route('/read_selected_stock', methods=['GET', 'POST'])
def read_selected_stock():
    stock_id = request.values.get('stock_id')
    stock_id = int(stock_id)
    selected_stock_list = member.add_selected_stock(stock_id)
    selected_stock_id_list = [selected_stock.get_stock_id() for selected_stock in selected_stock_list]
    return render_template('read_selected_stock.html', selected_stock_id_list=selected_stock_id_list)


@app.route('/set_calculate_profit_and_loss')
def set_calculate_profit_and_loss():
    return render_template('set_calculate_profit_and_loss.html')


@app.route('/calculate_profit_and_loss', methods=['GET', 'POST'])
def calculate_profit_and_loss():
    stock_id = request.form.get('stock_id')
    buy_price = request.form.get('buy_price')
    trading_volume = request.form.get('trading_volume')
    securities_firm = request.form.get('securities_firm')
    stock_id = int(stock_id)
    buy_price = float(buy_price)
    trading_volume = int(trading_volume)
    securities_firm = float(securities_firm)
    profit_and_loss = member.calculate_current_profit_and_loss(stock_id, buy_price, trading_volume, securities_firm)
    return render_template('calculate_profit_and_loss.html', profit_and_loss=profit_and_loss)


if __name__ == '__main__':
    # app.run()
    app.run(debug=True, port=5000)  # 存檔自動更新網頁
