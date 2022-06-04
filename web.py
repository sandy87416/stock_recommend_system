from time import sleep

import flask
import pandas as pd
from config import database_path
from flask import render_template, request, jsonify, redirect, url_for, session, flash
from config import app
from model.member.admin import Admin
from model.member.ordinary_member import OrdinaryMember
from model.member.premium_member import PremiumMember

user = None


@app.route('/menu')
def menu():
    if 'account' in session.keys():
        return render_template('menu.html')
    else:
        return redirect(url_for('index'))


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
    recommended_stock_list = user.read_recommended_stock(days, odds)
    json_data = jsonify(
        {'total': len(recommended_stock_list),
         'rows': recommended_stock_list[int(offset):(int(offset) + int(limit))]})
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
    stock_odds_list = user.read_stock_odds(stock_id)
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
    stock_after_hours_information = user.read_stock_after_hours_information(stock_id)
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
    stock_intraday_information = user.read_stock_intraday_information(stock_id)
    return render_template('read_stock_intraday_information.html',
                           stock_intraday_information=stock_intraday_information)


# UC-05 UC-13 UC-14
@app.route('/read_selected_stock', methods=['GET', 'POST'])
def read_selected_stock():
    selected_stock_list = user.read_selected_stock()
    if flask.request.method == 'GET':
        stock_id = request.values.get('selected_stock_id')
        selected_stock_list = user.delete_selected_stock(stock_id)
    elif flask.request.method == 'POST':
        stock_id = request.values.get('stock_id')
        stock_id = int(stock_id)
        selected_stock_list = user.add_selected_stock(stock_id)
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


# UC-10
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
    profit_and_loss = user.calculate_current_profit_and_loss(stock_id, buy_price, trading_volume, securities_firm)
    return render_template('calculate_current_profit_and_loss.html', profit_and_loss=profit_and_loss)


# UC-11
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
    profit_and_loss = user.calculate_profit_and_loss(buy_price, sell_price, trading_volume, securities_firm)
    return render_template('calculate_current_profit_and_loss.html', profit_and_loss=profit_and_loss)


# UC-12
@app.route('/read_stock_classification')
def read_stock_classification():
    stock_class_dict = user.read_stock_classification()
    return render_template('read_stock_classification.html', stock_class_dict=stock_class_dict)


def sign_up(account, password):
    member_df = pd.read_csv(database_path + 'member/member.csv')
    # 判斷帳號重複
    account_np = member_df['account'].to_numpy()
    if account in account_np:
        return '此帳號已經被註冊過'
    # 寫入member.csv
    member_df = pd.concat([member_df, pd.DataFrame({
        'account': [account],
        'password': [password],
        'level': [2],
    })])
    member_df.to_csv(database_path + 'member/member.csv', index=False)
    return '註冊成功'


# UC-07
@app.route('/register', methods=['GET', 'POST'])
def register():
    if flask.request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            flash('密碼與確認密碼不相符')
            return redirect(url_for('register'))
        register_message = sign_up(account, password)
        flash(register_message)
        if register_message == '註冊成功':
            return redirect(url_for('index'))
    return render_template('register.html')


def login(account, password):
    level = '-1'
    member_df = pd.read_csv(database_path + 'member/member.csv')
    member1_df = member_df[(member_df['account'] == account) & (member_df['password'] == password)]
    level_np = member1_df['level'].to_numpy()
    if len(level_np) > 0:
        level = str(level_np[0])
    if level == '0':
        return Admin(account, password), level
    elif level == '1':
        return PremiumMember(account, password), level
    elif level == '2':
        return OrdinaryMember(account, password), level
    else:
        return None, level


@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')
        print("account", account)
        print("password", password)
        global user
        user, level = login(account, password)
        if level != '-1':
            print("登入成功")
            session['account'] = user.get_account()
            session['level'] = level
            return redirect(url_for('menu'))
        else:
            print('登入失敗')
            flash('登入失敗')
            return redirect(url_for('index'))
    if 'account' in session.keys():
        return redirect(url_for('menu'))
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return render_template('login.html')


# UC-08
@app.route('/apply_premium_member', methods=['GET', 'POST'])
def apply_premium_member():
    if flask.request.method == 'POST':
        content = request.form.get('content')
        user.apply_premium_member(content)
        flash('申請成功')
        sleep(1)
        return redirect(url_for('menu'))
    return render_template('apply_premium_member.html')


# UC-09
@app.route('/upgrade_member_level', methods=['GET', 'POST'])
def upgrade_member_level():
    if flask.request.method == 'POST':
        account = request.form.get('account')
        user.upgrade_member_level(account)
        flash('升級成功')
        sleep(1)
        return redirect(url_for('upgrade_member_level'))
    application_information_zip = user.get_application_information_zip()
    return render_template('upgrade_member_level.html', application_information_zip=application_information_zip)


if __name__ == '__main__':
    # app.run()
    app.run(debug=True, port=5000)  # 存檔自動更新網頁
