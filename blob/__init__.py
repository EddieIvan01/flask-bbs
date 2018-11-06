from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from flask_login import LoginManager
#from flaskext.markdown import Markdown

app = Flask(__name__)
app.config.update(
    MONGO_URI = 'mongodb://flask:flask@127.0.0.1:27017/flask',
    SECRET_KEY = 'ck'
)

bootstrap = Bootstrap(app)
mongo = PyMongo(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'basic'
login_manager.login_view = 'routes.auth'

@app.errorhandler(404)
def handler_404(error):
    return render_template("404.html"), 200

@app.errorhandler(500)
def handler_500(error):
    return render_template("500.html"), 200
