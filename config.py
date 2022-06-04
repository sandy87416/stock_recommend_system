from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

root_path = 'F:/Courses/110-2/OOAD/'
database_path = root_path + 'stock_recommend_system/database/'
# database_path = root_path + 'stock/data/'

app = Flask(__name__)
bootstrap = Bootstrap(app)
# https://www.796t.com/p/461428.html
app.config['SECRET_KEY'] = b'\x1f\x92\xcc\x81\x1e\x972h\x89\x0e\xaaC\xdc+lh\xed5\xe8,\xf5>\xec~'
login = LoginManager(app)
login.login_view = 'login'
login.login_message = 'You must login to access this page'
login.login_message_category = 'info'