import flask
from flask_bootstrap import Bootstrap
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
    odds = int(odds) / 10
    recommended_stock_list = current_user.read_recommended_stock(days, odds)
    return jsonify(recommended_stock_list)


@app.route('/query_specific_stock_page')
def query_specific_stock_page():
    return render_template('query_specific_stock_page.html')


# UC-02
@app.route('/read_stock_odds', methods=['GET', 'POST'])
def read_stock_odds():
    stock_id = int(request.values.get('stock_id'))
    stock_odds_list = current_user.read_stock_odds(stock_id)
    return jsonify(stock_odds_list)


@app.route('/stock_information_menu')
def stock_information_menu():
    return render_template('stock_information_menu.html')


@app.route('/stock_after_hours_information_page')
def stock_after_hours_information_page():
    return render_template('stock_after_hours_information_page.html', stock_after_hours_information_dict=dict())


# UC-03
@app.route('/read_stock_after_hours_information', methods=['GET', 'POST'])
def read_stock_after_hours_information():
    stock_id = int(request.form.get('stock_id', 0))
    stock_after_hours_information_dict = dict()
    if stock_system.check_stock_id(stock_id):
        stock_after_hours_information = current_user.read_stock_after_hours_information(stock_id)
        stock_after_hours_information_dict["monthly_revenue"] = stock_after_hours_information.get_monthly_revenue()
        stock_after_hours_information_dict["k_value"] = stock_after_hours_information.get_k_value()
        stock_after_hours_information_dict["ma20_value"] = stock_after_hours_information.get_ma20_value()
        stock_after_hours_information_dict["rsi_value"] = stock_after_hours_information.get_rsi_value()
        stock_after_hours_information_dict["foreign_buy"] = stock_after_hours_information.get_foreign_buy()
        stock_after_hours_information_dict["investment_trust_buy"] = stock_after_hours_information.get_investment_trust_buy()
        stock_after_hours_information_dict["self_buy"] = stock_after_hours_information.get_self_buy()
        stock_after_hours_information_dict["news"] = stock_after_hours_information.get_news()
        if len(stock_after_hours_information_dict) == 0:
            flash("查無股票資料", 'danger')
    else:
        flash('查無此股票代號', 'warning')
    return render_template('stock_after_hours_information_page.html', stock_after_hours_information_dict=stock_after_hours_information_dict)


@app.route('/query_stock_intraday_information_page')
def query_stock_intraday_information_page():
    return render_template('query_stock_intraday_information_page.html')


# UC-04
@app.route('/read_stock_intraday_information')
def read_stock_intraday_information():
    stock_id = int(request.values.get('stock_id', '0'))
    stock_intraday_information_dict = dict()
    if stock_id != '0' and stock_system.check_stock_id(stock_id):
        stock_intraday_information = current_user.read_stock_intraday_information(stock_id)
        stock_intraday_information_dict['open_price'] = stock_intraday_information.get_open_price()
        stock_intraday_information_dict['high_price'] = stock_intraday_information.get_high_price()
        stock_intraday_information_dict['low_price'] = stock_intraday_information.get_low_price()
        stock_intraday_information_dict['close_price'] = stock_intraday_information.get_close_price()
    else:
        return ''
    if len(stock_intraday_information_dict) == 0:
        return ''
    stock_intraday_information_list = [stock_intraday_information_dict]
    stock_intraday_information = jsonify(
        {'total': len(stock_intraday_information_list), 'rows': stock_intraday_information_list})
    return stock_intraday_information


# UC-05
@app.route('/read_selected_stock_page', methods=['GET'])
def read_selected_stock_page():
    return render_template('read_selected_stock.html')


# UC-05
@app.route('/read_selected_stock', methods=['GET'])
def read_selected_stock():
    selected_stock_list = current_user.read_selected_stock()
    selected_stock_list = [{'stock_id': str(selected_stock.get_stock_id())}
                           for selected_stock in selected_stock_list]
    return jsonify(selected_stock_list)


# UC-13
@app.route('/add_selected_stock', methods=['GET'])
def add_selected_stock():
    selected_stock_list = list()
    stock_id = int(request.values.get('stock_id'))
    if stock_system.check_stock_id(stock_id):
        selected_stock_list1 = current_user.add_selected_stock(stock_id)
        selected_stock_list = [{'stock_id': str(selected_stock.get_stock_id())}
                               for selected_stock in selected_stock_list1]
    else:
        flash('查無此股票代號', 'warning')
    return jsonify(selected_stock_list)


# UC-14
@app.route('/delete_selected_stock', methods=['POST'])
def delete_selected_stock():
    stock_id = request.values.get('selected_stock_id')
    # selected_stock_list =
    current_user.delete_selected_stock(stock_id)
    # selected_stock_id_list = [selected_stock.get_stock_id() for selected_stock in selected_stock_list]
    # return render_template('read_selected_stock.html', selected_stock_id_list=selected_stock_id_list)


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
        flash('查無此股票代號', 'warning')
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


@app.route('/query_stock_classification_page')
def query_stock_classification_page():
    return render_template('read_stock_classification.html')


# UC-12
@app.route('/read_stock_classification')
def read_stock_classification():
    stock_class_dict = current_user.read_stock_classification()
    stock_classification_list = list()
    for stock_class in stock_class_dict:
        stock_list = stock_class_dict[stock_class]
        for stock in stock_list:
            stock_classification_dict = dict()
            stock_classification_dict["stock_class"] = stock_class
            stock_classification_dict["stock_id"] = stock[-4:]
            stock_classification_dict["stock_name"] = stock[:-5]
            stock_classification_list.append(stock_classification_dict)
    return jsonify(stock_classification_list)


# UC-07
@app.route('/register', methods=['GET', 'POST'])
def register():
    if flask.request.method == 'POST':
        id = request.form.get('id')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            flash('密碼與確認密碼不相符', 'warning')
            return redirect(url_for('register'))
        register_message = User().register(id, password)
        flash(register_message, 'danger')
        if register_message == '註冊成功':
            return redirect(url_for('index'))
    return render_template('register.html')


# UC-08
@app.route('/apply_premium_member', methods=['GET', 'POST'])
def apply_premium_member():
    content = ''
    if flask.request.method == 'GET':
        content = current_user.get_apply_content()
    elif flask.request.method == 'POST':
        content = request.form.get('content')
        current_user.apply_premium_member(content)
        flash("sent", 'success')
    return render_template('apply_premium_member.html', content=content)


# UC-09
@app.route('/upgrade_member_level_page', methods=['GET'])
def upgrade_member_level_page():
    return render_template('upgrade_member_level.html')


@app.route('/read_application_information', methods=['GET'])
def read_application_information():
    application_information_list = current_user.get_application_information_list()
    data_list = list()
    for application_information in application_information_list:
        application_information_dict = dict()
        application_information_dict["id"] = str(application_information.get_id())
        application_information_dict["content"] = application_information.get_content()
        data_list.append(application_information_dict)
    return jsonify(data_list)


@app.route('/upgrade_member_level', methods=['POST'])
def upgrade_member_level():
    id = request.form.get('id')
    current_user.upgrade_member_level(id)
    return "升級成功!"


@app.route('/delete_application_information', methods=['POST'])
def delete_application_information():
    id = request.form.get('id')
    current_user.delete_application_information_data(id)
    return "刪除成功!"


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
            flash('登入失敗', 'warning')
            return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    current_user.logout()
    return render_template('login.html')


if __name__ == '__main__':
    # app.run()
    app.run(debug=True, port=5000)  # 存檔自動更新網頁
