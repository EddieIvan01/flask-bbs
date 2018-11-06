from .. import mongo
from .escape import flask_real_escape

from flask_login import login_required
from flask import render_template, Blueprint, Response, request
import base64

main = Blueprint("head_img", __name__)

@main.route("/head-img/<user>")
def head_img(user):
    user, flag = flask_real_escape(user)
    if flag:
        return "Sqli detection"
    try:
        _img = mongo.db.image.find_one({"uname": user})["img"].decode("utf-8")
        img = base64.b64decode(_img)
        return Response(img, mimetype="image/jpg")
    except:
        return Response(b"", mimetype="image/jpg")