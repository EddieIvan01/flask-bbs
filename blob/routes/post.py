from ..utils.get_posts import get_posts_api
from ..utils.escape import xss_escape, flask_real_escape
from .. import mongo

from flask import render_template, Blueprint, request, flash, redirect
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Required
import time
from bson.objectid import ObjectId

main = Blueprint("post", __name__)

def sec2time(i):
    return time.asctime(time.localtime(int(i)))

class CommentForm(FlaskForm):
    
    comment = TextAreaField("Say something?")
    submit = SubmitField("OK")

@main.route("/post", methods=["POST", "GET"])
@login_required
def post_handler():
    if request.form:
        md_data = request.form.get("test-editormd-markdown-doc")
        title = md_data.split("\n")[0].strip("#").strip(" ").strip("\r")
        md_data = ''.join(md_data.split("\n")[1:])
        md_data = xss_escape(md_data)
        mongo.db.posts.insert_one({
            "title": title, 
            "content": md_data, 
            "comments": [], 
            "author": current_user.uname, 
            "date": int(time.time())
        })
        flash("Post artical success!")
        return redirect('/')
    return render_template("post.html")

@main.route("/posts/t/<id>", methods=["POST", "GET"])
def posts_handler(id):
    form = CommentForm()
    if request.args.get("act")=="delete":
        try:
            if current_user.is_anonymous:
                return "Anonymous user want to delete others' posts?", 401
            id, _= flask_real_escape(id)
            author = mongo.db.posts.find_one({"_id": ObjectId(id)})["author"]
            if author == current_user.uname or current_user.is_admin():
                mongo.db.posts.remove({"_id": ObjectId(id)})
                flash("Delete success!")
                return redirect("/")
            else:
                return "Let me guess, U want to delete others' posts?", 401
        except:
            return redirect("/posts/t/"+str(id))
    try:
        if form.validate_on_submit():
            if current_user.is_anonymous:
                flash("Login first!")
                return redirect("/auth/login")
            comment = form.comment.data
            comment, _ = flask_real_escape(comment)        
            id, _ = flask_real_escape(id)
            mongo.db.posts.update({
                "_id": ObjectId(id)
                }, 
                {"$push": 
                 {"comments": 
                  {"user": current_user.uname, 
                   "content": comment, 
                   "date": int(time.time())
                   }
                  }
                 })
            form.comment.data=""
            flash("Comment success!")
            return redirect("/posts/t/"+str(id))
    except:
        return redirect("/posts/t/"+str(id))
    if request.args.get("act")=="delete-comment" and request.args.get("a") and request.args.get("t"):
        try:
            a = request.args.get("a")
            t = request.args.get("t")
            if current_user.is_anonymous:
                return "Anonymous user!!", 401
            if current_user.uname!=a and not current_user.is_admin():
                return "No no no, dude, learn to accept others' opinions", 401
            id, _ = flask_real_escape(id)
            a, _ = flask_real_escape(a)
            t, _ = flask_real_escape(t)
            comment_list = mongo.db.posts.find_one({"_id": ObjectId(id)})["comments"]
            target = None
            for i in comment_list:
                if i["user"]==a and str(i["date"])==t:
                    target = i
                    break
            if target:
                mongo.db.posts.update({"_id": ObjectId(id)}, {"$pull": {"comments": {"user": a, "date": int(t)}}})
                return redirect("/posts/t/"+str(id))
            else:
                raise Exception
        except:
            return "What are you request to delete??", 400
    post = get_posts_api(_id=ObjectId(id))[0]
    return render_template("posts.html", post=post, form=form, convert=sec2time)
