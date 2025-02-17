from flask import Flask, render_template, request, url_for, redirect, session
# from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
#user_unauthorized, user_logged_in, user_logged_out
#from flask_login import FlaskLoginClient as LoginClient
# from flask_user import current_user, login_required, roles_required

from utils import roles_required
# from models import db, Users
# from db import db
#from init_db import db
#import flask_migrate as migration
#from .models.user_models import Users

import logging
import os

blueprint = Flask(__name__)
blueprint.config.from_object("config")

logging.basicConfig(filename='errors.log', level=logging.DEBUG)
login_manager = LoginManager()
login_manager.init_app(blueprint)

# # db, User defs here
from mymodels import db, Users
db.init_app(blueprint)

with blueprint.app_context():
    db.create_all()

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

@blueprint.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        first_name = request.form.get("firstname")
        last_name = request.form.get("lastname")
        pswd = request.form.get("password")
        pswd_hash = pswd  ## Hash the password before saving

        if not first_name or not last_name:
            user = Users(
                username = username,
                password = pswd_hash
            )
        elif not username:
            pass
        elif not pswd:
            pass
        else:
            user = Users(
                username = request.form.get("username"),
                password = pswd_hash,
                first_name = request.form.get("firstname"),
                last_name = request.form.get("lastname")
            )

        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("sign_up.html")

@blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(username = request.form.get("username")).first()
        # Get password hash and convert and shit
        if user.password == request.form.get("password"):
            login_user(user)
            session['is_logged_in'] = True
            session["active_user"] = user.id

            blueprint.logger.info(f"User session:  {session["active_user"]}")
            #return redirect(url_for("home"))
            return redirect(url_for("main_page"))
        else:
            # # Wrong password.
            # is_logged_in = session.get('is_logged_in', False)
            # blueprint.logger.info(f"is_logged_in:  {is_logged_in}")
            return render_template("index.html", is_logged_in=False, role='pswd-fail')

    is_logged_in = session.get('is_logged_in', False)
    return render_template("index.html", is_logged_in=is_logged_in, role='none')

@blueprint.route("/logout")
def logout():
    logout_user()
    session['is_logged_in'] = False
    session["active_user"] = None
    return redirect(url_for("home"))

@blueprint.route("/")
def home():
    is_logged_in = session.get('is_logged_in', False)
    return render_template("index.html", is_logged_in=is_logged_in, role='admin')

@blueprint.route("/home")
def main_page():
    # get the user's role.
    role_placeholder = 'admin'
    return render_template("main.html", is_logged_in=True, role=role_placeholder)

@blueprint.route("/team-manager")
@login_required
def team_manager():
    return None

@blueprint.route("/asset-information")
@login_required
def asset_information():
    return None

@blueprint.route("/schedule-manager")
@login_required
def schedule_manager():
    return None

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for(""))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    blueprint.run(host="0.0.0.0", port=port)