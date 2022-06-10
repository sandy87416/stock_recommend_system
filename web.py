import flask
import pandas as pd
from flask_bootstrap import Bootstrap
from time import sleep
from config import database_path
from model import member_system, stock_system
from model.member.user import User
from model.member.member import Member
from flask_login import login_user, current_user, LoginManager
from flask import render_template, request, jsonify, redirect, url_for, flash, Flask, session

app = Flask(__name__)
bootstrap = Bootstrap(app)
# https://www.796t.com/p/461428.html
app.config['SECRET_KEY'] = b'\x1f\x92\xcc\x81\x1e\x972h\x89\x0e\xaaC\xdc+lh\xed5\xe8,\xf5>\xec~'
login = LoginManager(app)
login.login_view = 'login'
login.login_message = 'You must login to access this page'
login.login_message_category = 'info'


@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/stock_odds_menu')
def stock_odds_menu():
    return render_template('stock_odds_menu.html')


@app.route('/query_recommended_stock_page')
def query_recommended_stock_page():
    return render_template('query_recommended_stock_page.html')


# UC-01
@app.route('/read_recommended_stock', methods=['GET', 'POST'])
def read_recommended_stock():
    days = int(request.values.get('days'))
    odds = int(request.values.get('odds'))
    limit = request.values.get('limit', 10)
    offset = request.values.get('offset', 1)
    odds = int(odds) / 10
    recommended_stock_list = current_user.read_recommended_stock(days, odds)
    json_data = jsonify(
        {'total': len(recommended_stock_list), 'rows': recommended_stock_list[int(offset):(int(offset) + int(limit))]})
    return json_data


@app.route('/query_specific_stock_page')
def query_specific_stock_page():
    return render_template('query_specific_stock_page.html')


# UC-02
@app.route('/read_stock_odds', methods=['GET', 'POST'])
def read_stock_odds():
    stock_id = request.values.get('stock_id')  # todo: 輸入資料庫沒有的股票
    limit = request.values.get('limit', 10)
    offset = request.values.get('offset', 1)
    stock_id = int(stock_id)
    stock_odds_list = current_user.read_stock_odds(stock_id)
    json_data = jsonify(
        {'total': len(stock_odds_list), 'rows': stock_odds_list[int(offset):(int(offset) + int(limit))]})
    return json_data


@app.route('/stock_information_menu')
def stock_information_menu():
    return render_template('stock_information_menu.html')


@app.route('/set_stock_id_read_stock_after_hours_information')  # todo: 不要跳轉
def set_stock_id_read_stock_after_hours_information():
    return render_template('set_stock_id_read_stock_after_hours_information.html')


# UC-03
@app.route('/read_stock_after_hours_information', methods=['GET', 'POST'])
def read_stock_after_hours_information():
    stock_id = request.values.get('stock_id')
    stock_id = int(stock_id)
    if stock_system.check_stock_id(stock_id):
        stock_after_hours_information = current_user.read_stock_after_hours_information(stock_id)
    else:
        flash("查無股票資料")
        return redirect(url_for('set_stock_id_read_stock_after_hours_information'))
    return render_template('read_stock_after_hours_information.html',
                           stock_after_hours_information=stock_after_hours_information)


@app.route('/set_stock_id_read_stock_intraday_information')  # todo: rename
def set_stock_id_read_stock_intraday_information():
    return render_template('set_stock_id_read_stock_intraday_information.html')


# UC-04
@app.route('/read_stock_intraday_information', methods=['GET', 'POST'])
def read_stock_intraday_information():
    stock_id = request.values.get('stock_id')
    stock_id = int(stock_id)
    if stock_system.check_stock_id(stock_id):
        stock_intraday_information = current_user.read_stock_intraday_information(stock_id)
    else:
        flash("查無股票資料")
        return redirect(url_for('set_stock_id_read_stock_intraday_information'))
    return render_template('read_stock_intraday_information.html',
                           stock_intraday_information=stock_intraday_information)


# UC-05 UC-13
@app.route('/read_selected_stock', methods=['GET', 'POST'])
def read_selected_stock():
    selected_stock_list = list()
    if flask.request.method == 'GET':
        selected_stock_list = current_user.read_selected_stock()
    elif flask.request.method == 'POST':
        stock_id = int(request.values.get('stock_id'))
        if stock_system.check_stock_id(stock_id):
            selected_stock_list = current_user.add_selected_stock(stock_id)
        else:
            flash('查無此股票代號')
            selected_stock_list = current_user.read_selected_stock()
            selected_stock_id_list = [selected_stock.get_stock_id() for selected_stock in selected_stock_list]
            return render_template('read_selected_stock.html', selected_stock_id_list=selected_stock_id_list)
    selected_stock_id_list = [selected_stock.get_stock_id() for selected_stock in selected_stock_list]
    return render_template('read_selected_stock.html', selected_stock_id_list=selected_stock_id_list)


# UC-14
@app.route('/delete_selected_stock', methods=['POST'])
def delete_selected_stock():
    stock_id = request.values.get('selected_stock_id')
    selected_stock_list = current_user.delete_selected_stock(stock_id)
    selected_stock_id_list = [selected_stock.get_stock_id() for selected_stock in selected_stock_list]
    return render_template('read_selected_stock.html', selected_stock_id_list=selected_stock_id_list)


@app.route('/calculate_profit_and_loss_page')
def calculate_profit_and_loss_page():
    return render_template('calculate_profit_and_loss_page.html')


# UC-10
@app.route('/calculate_current_profit_and_loss', methods=['POST'])
def calculate_current_profit_and_loss():
    current_profit_and_loss = 0
    stock_id = int(request.form.get('stock_id'))
    buy_price = float(request.form.get('buy_price'))
    trading_volume = int(request.form.get('trading_volume'))
    securities_firm = float(request.form.get('securities_firm'))
    if stock_system.check_stock_id(stock_id):
        current_profit_and_loss = current_user.calculate_current_profit_and_loss(stock_id, buy_price, trading_volume,
                                                                                 securities_firm)
    else:
        flash('查無此股票代號')
        return render_template('calculate_profit_and_loss_page.html', current_profit_and_loss=current_profit_and_loss)
    return render_template('calculate_profit_and_loss_page.html', current_profit_and_loss=current_profit_and_loss)


# UC-11
@app.route('/calculate_profit_and_loss', methods=['POST'])
def calculate_profit_and_loss():
    buy_price = float(request.form.get('buy_price'))
    sell_price = float(request.form.get('sell_price'))
    trading_volume = int(request.form.get('trading_volume'))
    securities_firm = float(request.form.get('securities_firm'))
    profit_and_loss = current_user.calculate_profit_and_loss(buy_price, sell_price, trading_volume, securities_firm)
    return render_template('calculate_profit_and_loss_page.html', profit_and_loss=profit_and_loss)


# UC-12
@app.route('/read_stock_classification')
def read_stock_classification():
    stock_class_dict = current_user.read_stock_classification()
    return render_template('read_stock_classification.html', stock_class_dict=stock_class_dict)


# UC-07
@app.route('/register', methods=['GET', 'POST'])
def register():
    if flask.request.method == 'POST':
        id = request.form.get('id')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            flash('密碼與確認密碼不相符')
            return redirect(url_for('register'))
        register_message = User().register(id, password)
        flash(register_message)
        if register_message == '註冊成功':
            return redirect(url_for('index'))
    return render_template('register.html')


# UC-08
@app.route('/apply_premium_member', methods=['GET', 'POST'])
def apply_premium_member():
    if flask.request.method == 'POST':
        content = request.form.get('content')
        current_user.apply_premium_member(content)
        flash('申請成功')
        sleep(1)
        return redirect(url_for('menu'))
    return render_template('apply_premium_member.html')


# UC-09
@app.route('/upgrade_member_level', methods=['GET', 'POST'])
def upgrade_member_level():
    application_information_list = list()
    if flask.request.method == 'GET':
        application_information_list = current_user.get_application_information_list()
    elif flask.request.method == 'POST':
        action_id = request.form.get('id')
        action_id_split = action_id.split(' ')
        action = action_id_split[0]
        id = action_id_split[1]
        if action == '升級':
            application_information_list = current_user.upgrade_member_level(id)
        elif action == '刪除':
            current_user.delete_application_information_data(id)
            application_information_list = current_user.get_application_information_list()
    return render_template('upgrade_member_level.html', application_information_list=application_information_list)


@login.user_loader
def load_user(id):
    user, level = User().login(id)
    session['level'] = level
    return user


@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'POST':
        id = request.form.get('id')
        password = request.form.get('password')
        if member_system.is_id_and_password_validate(id, password):
            login_user(Member(id, password))
            return redirect(url_for('menu'))
        else:
            flash('登入失敗')
            return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    current_user.logout()
    return render_template('login.html')


if __name__ == '__main__':
    # app.run()
    app.run(debug=True, port=5000)  # 存檔自動更新網頁
