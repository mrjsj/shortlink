from concurrent.futures import thread
from flask import Flask, Blueprint, redirect, render_template, session, request, flash
from .commands import create_tables
from .extensions import db, login_manager
from .models import User, Link
#from .routes.auth import auth
from flask_session import Session
import hashlib


main = Blueprint('main', __name__)

def create_app(config_file="settings.py"):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    app.register_blueprint(main)
    #app.register_blueprint(auth)

    app.cli.add_command(create_tables)
    return app


@main.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@main.route("/l/<shortlink>")
def l(shortlink):
    result = Link.query.filter(Link.shortlink == shortlink).first()
    return redirect(result.link)


@main.route("/", methods=["GET", "POST"])
def index():
    # TODO: If user is logged in store his id in session cookie

    # TODO: If user logs in clear session data and populate with links from db for that user

    # TODO: Add ability to delete link

    # TODO: Add scheduled cleansing of database. E.g. removes links which haven't been used in X days
    # This would require a change to route /l/ in which a column "last_accessed" is updated
    # Then run a cron job which evaluates every 24 hours to see if last_accessed is more than 30 days old

    if len(session["data"]) == 0:
        session["data"] = []

    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            flash("Invalid Url", "error")

        if not url.startswith("https://") and not url.startswith("http://"):
            flash("Url must start with http:// or https:// !", "error")
            return render_template("index.html", data=session["data"], baseurl=request.base_url+'l/')

        # Hash the url to 8 characters
        shortlink = hashlib.shake_256(url.encode()).hexdigest(4)

        # Store link in database
        link = Link(
            link = url,
            user_id = 0,
            shortlink=shortlink
        )

        db.session.add(link)
        db.session.commit()

        # Store link in users session cookie
        link_json = {
            "link" : url,
            "shortlink" : shortlink
        }
        session["data"].append(link_json)
    
    return render_template("index.html", data=session["data"], baseurl=request.base_url+'l/')

if __name__ == "__main__":
    app = create_app()
    Session(app)
    app.run(host="127.0.0.1", threaded=True)