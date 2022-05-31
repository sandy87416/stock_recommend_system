import flask
from flask import render_template, request, jsonify, redirect, url_for, session
from config import app
from model.member.admin import Admin
from model.member.member import Member
from model.member.ordinary_member import OrdinaryMember
from model.member.premium_member import PremiumMember
from model.member.user import User

# premium_member =
user = User()


@app.route('/menu')
def menu():
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
    premium_member = PremiumMember(session['account'], session['password'])
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
    premium_member = PremiumMember(session['account'], session['password'])
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
    member = Member(session['account'], session['password'])
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
    member = Member(session['account'], session['password'])
    stock_intraday_information = member.read_stock_intraday_information(stock_id)
    return render_template('read_stock_intraday_information.html',
                           stock_intraday_information=stock_intraday_information)


@app.route('/delete_selected_stock')  # todo: delete_selected_stock
def delete_selected_stock():
    return render_template('add_selected_stock.html')


@app.route('/read_selected_stock', methods=['GET', 'POST'])
def read_selected_stock():
    member = Member(session['account'], session['password'])
    selected_stock_list = member.read_selected_stock()
    if flask.request.method == 'GET':
        stock_id = request.values.get('selected_stock_id')
        selected_stock_list = member.delete_selected_stock(stock_id)
    elif flask.request.method == 'POST':
        stock_id = request.values.get('stock_id')
        stock_id = int(stock_id)
        selected_stock_list = member.add_selected_stock(stock_id)
    selected_stock_id_list = [selected_stock.get_stock_id() for selected_stock in selected_stock_list]
    return render_template('read_selected_stock.html', selected_stock_id_list=selected_stock_id_list)


@app.route('/calculate_profit_and_loss_menu')
def calculate_profit_and_loss_menu():
    return render_template('calculate_profit_and_loss_menu.html')


@app.route('/set_current_calculate_profit_and_loss')
def set_current_calculate_profit_and_loss():
    return render_template('set_current_calculate_profit_and_loss.html')


@app.route('/set_calculate_profit_and_loss')
def set_calculate_profit_and_loss():
    return render_template('set_calculate_profit_and_loss.html')


@app.route('/calculate_current_profit_and_loss', methods=['GET', 'POST'])
def calculate_current_profit_and_loss():
    stock_id = request.form.get('stock_id')
    buy_price = request.form.get('buy_price')
    trading_volume = request.form.get('trading_volume')
    securities_firm = request.form.get('securities_firm')
    stock_id = int(stock_id)
    buy_price = float(buy_price)
    trading_volume = int(trading_volume)
    securities_firm = float(securities_firm)
    member = Member(session['account'], session['password'])
    profit_and_loss = member.calculate_current_profit_and_loss(stock_id, buy_price, trading_volume, securities_firm)
    return render_template('calculate_current_profit_and_loss.html', profit_and_loss=profit_and_loss)


@app.route('/calculate_profit_and_loss', methods=['GET', 'POST'])
def calculate_profit_and_loss():
    buy_price = request.form.get('buy_price')
    sell_price = request.form.get('sell_price')
    trading_volume = request.form.get('trading_volume')
    securities_firm = request.form.get('securities_firm')
    buy_price = float(buy_price)
    sell_price = float(sell_price)
    trading_volume = int(trading_volume)
    securities_firm = float(securities_firm)
    member = Member(session['account'], session['password'])
    profit_and_loss = member.calculate_profit_and_loss(buy_price, sell_price, trading_volume, securities_firm)
    return render_template('calculate_current_profit_and_loss.html', profit_and_loss=profit_and_loss)


@app.route('/read_stock_classification')
def read_stock_classification():
    member = Member(session['account'], session['password'])
    stock_class_dict = member.read_stock_classification()
    return render_template('read_stock_classification.html', stock_class_dict=stock_class_dict)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if flask.request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        register_message = user.register(account, password)
        if password == confirm_password and register_message == '註冊成功':
            return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')
        login_message, level = user.login(account, password)
        if login_message == '登入成功':
            session['account'] = str(account)
            session['password'] = str(password)
            session['level'] = str(level)
            return redirect(url_for('menu'))
        else:
            return render_template('login.html')
    if 'account' in session.keys():
        return redirect(url_for('menu'))
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return render_template('login.html')


@app.route('/apply_premium_member', methods=['GET', 'POST'])
def apply_premium_member():
    if flask.request.method == 'POST':
        ordinary_member = OrdinaryMember(session['account'], session['password'])
        content = request.form.get('content')
        ordinary_member.apply_premium_member(content)  # todo:alert 申請成功
        return redirect(url_for('menu'))
    return render_template('apply_premium_member.html')


@app.route('/upgrade_member_level', methods=['GET', 'POST'])
def upgrade_member_level():
    admin = Admin(session['account'], session['password'])
    if flask.request.method == 'POST':
        account = request.form.get('account')
        admin.upgrade_member_level(account)  # todo:alert 申請成功
        return redirect(url_for('upgrade_member_level'))
    application_information_zip = admin.get_application_information_zip()
    return render_template('upgrade_member_level.html', application_information_zip=application_information_zip)


if __name__ == '__main__':
    # app.run()
    app.run(debug=True, port=5000)  # 存檔自動更新網頁
