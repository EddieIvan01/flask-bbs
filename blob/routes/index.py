from ..utils.get_posts import get_posts_api, get_posts_count
from .post import sec2time

from flask import Blueprint, render_template, request
import re

main = Blueprint('index', __name__)

@main.route("/", methods=["POST", "GET"])
def index_handler():
    page = request.args.get("page")
    if not page:
        page = 1
    if re.findall(r"[^1-9]", str(page)):
        return "Sqli detection", 401
    if int(page) >= 2**32:
        return "You think Python could overflow??"
    posts_list = get_posts_api(limit=10, skip=(int(page)-1)*10)
    return render_template("index.html", posts=posts_list, convert=sec2time, page=int(page), count=int(get_posts_count()/10+1))

@main.route("/about", methods=["GET"])
def about():
    return render_template("about.html")
