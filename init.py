import sys,os,flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

project_path = "/dpooj"
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path) + project_path,
                                                               os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WORKPLACE_FOLDER']='./static/workplace'
app.config['DEBUG_PATH']='./debug'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
print("dpooj server started")

@login_manager.user_loader
def load_user(user_id):
    from models import User
    user = User.query.get(int(user_id))
    return user


login_manager.login_view = 'login'
# login_manager.login_message = 'Your custom message'


@app.context_processor
def inject_user():
    from models import User
    user = User.query.first()
    return dict(user=user)

