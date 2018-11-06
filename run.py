from blob import app
from blob.routes import auth_handler
from blob.routes import index_handler
from blob.routes import user_handler
from blob.routes import post_handler
from blob.utils.head_img import main as head_img

if __name__ == "__main__":
    app.register_blueprint(auth_handler, url_prefix="/auth")
    app.register_blueprint(index_handler)
    app.register_blueprint(user_handler, url_prefix="/user")
    app.register_blueprint(post_handler)
    app.register_blueprint(head_img)
    app.run(host="127.0.0.1", port=2333, debug=True)
