from .. import mongo, app
from ..models import BaseUser
from ..utils.escape import flask_real_escape, flask_real_escape_list

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Email, EqualTo, Required
from flask_login import login_required, login_user, logout_user
import base64
import random
import hashlib

main = Blueprint('auth', __name__)
anonymous_head_img = base64.b64encode(open("blob/static/img/head.jpg", "rb").read())
salt = app.config["SECRET_KEY"]
captcha_operators = ["+", "-", "*"]
captcha = str(random.randint(1, 10))+random.choice(captcha_operators)+\
    str(random.randint(1, 10))+random.choice(captcha_operators)+\
    str(random.randint(1, 10))+random.choice(captcha_operators)+str(random.randint(1, 10))

class RegisterForm(FlaskForm):
    
    uname = StringField("UserName: ", validators=[Required()])
    passwd = PasswordField("Password: ", validators=[Required()])
    passwd_2 = PasswordField("Verify your password: ", validators=[Required(), EqualTo("passwd", "Password is not same")])
    email = StringField("Email: ", validators=[Required(), Email()])
    captcha = StringField("Captcha: "+captcha+"=", validators=[Required()])
    submit = SubmitField()

class LoginForm(FlaskForm):
    
    uname = StringField("UserName: ", validators=[Required()])
    passwd = PasswordField("Password: ", validators=[Required()])
    remember = BooleanField("Remember me: ")
    submit = SubmitField()
    
@main.route("/login", methods=["GET", "POST"])
def login_handler():
    form = LoginForm()
    if form.validate_on_submit():
        uname = form.uname.data
        passwd = form.passwd.data
        remember = form.remember.data
        tmp, flag = flask_real_escape_list([uname, passwd])
        if flag:
            return "Sqli detection"
        uname, passwd = tmp
        result = mongo.db.users.find_one({"uname": uname})
        if result and BaseUser.verify_passwd(passwd, result["passwd"]):
            user = BaseUser(result["_id"], uname, passwd, result["email"], result["role"])
            login_user(user, remember)
            return redirect(url_for("index.index_handler"))
        flash("Invalid username or password")
        form.uname.data = ""
        form.passwd.data = ""
    return render_template("auth/login.html", form=form)

@main.route("/register", methods=["GET", "POST"])
def register_handler():
    form = RegisterForm()
    try:
        fp = open("captcha.txt", "r")
    except:
        fp = open("captcha.txt", "w+")
        fp.write("1+1")
    private_captcha = fp.read()
    fp.close()
    with open("captcha.txt", "w") as fp:
        fp.write(captcha)
    if form.validate_on_submit():
        if str(form.captcha.data) != str(eval(private_captcha)):
            flash("Captcha wrong")
            return redirect(url_for('auth.register_handler'))
        uname = form.uname.data
        passwd = form.passwd.data
        email = form.email.data
        tmp, flag = flask_real_escape_list([uname, passwd, email])
        if flag:
            return "Sqli detection"
        uname, passwd, email = tmp        
        try:
            mongo.db.users.insert_one({
                "uname": uname, 
                "passwd": BaseUser.hash_passwd(passwd, salt), 
                "email": email, 
                "role": "basic"
            })
            mongo.db.image.insert_one({
                "uname": uname, 
                "img": anonymous_head_img
            })
            mongo.db.info.insert_one({
                "uname": uname,
                "email": "",
                "blog": "",
                "github": "",
                "phone": "",
                "qq": ""
            })
            flash("Register success! You can login now")
            return redirect(url_for('auth.login_handler'))
        except:
            flash("Username is already registered")
    return render_template("auth/register.html", form=form)

@main.route("/logout", methods=["GET", "POST"])
def logout_handler():
    logout_user()
    return redirect("/")