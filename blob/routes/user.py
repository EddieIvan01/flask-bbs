from .. import mongo
from ..utils.escape import flask_real_escape, flask_real_escape_list

from flask import render_template, Blueprint, flash, redirect
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SubmitField
from wtforms.validators import Required, Email, URL
import base64

main = Blueprint("user", __name__)  

class ModifyForm(FlaskForm):
    
    head_img = FileField("Head IMG", validators=[Required()])
    email = StringField("Email: ", validators=[Email()])
    blog = StringField("Blog: ", validators=[URL()])
    github = StringField("Github: ", validators=[URL()])
    phone = StringField("Phone: ")
    qq = StringField("QQ: ")
    submit = SubmitField("Upload")

def set_head_img(mongodb, uname, s):
    s = base64.b64encode(s)
    mongodb.db.image.update({"uname": uname}, {"$set": {"img": s}})
        
@main.route("/<uname>", methods=["GET", "POST"])
def u_info_handler(uname):
    if current_user.is_anonymous:
        flash("Login first!!")
        return redirect("/auth/login")
    form = ModifyForm()
    if form.validate_on_submit():
        if uname != current_user.uname and not current_user.is_admin():
            return "Let me guess!<br />U are trying to modify others' personal information?", 401        
        data = form.head_img.data.read()
        set_head_img(mongo, uname, data)   
        email = form.email.data
        blog = form.blog.data
        github = form.github.data
        phone = form.phone.data
        qq = form.qq.data
        tmp, _ = flask_real_escape_list([email, phone, qq])
        email, phone, qq = tmp
        mongo.db.info.update({
            "uname": uname
            }, 
            {"$set":{
                "email": email, 
                "blog": blog, 
                "github": github, 
                "phone": phone, 
                "qq": qq
            }
        })
        flash("Update success")
        form.email.data = ""
        form.blog.data = ""
        form.github.data = ""
        form.phone.data = ""
        form.qq.data = ""
    uname, _ = flask_real_escape(uname)
    user_obj  = mongo.db.users.find_one({"uname": uname})
    info = mongo.db.info.find_one({"uname": uname})
    return render_template("user.html", form=form, user_obj=user_obj, info=info)
