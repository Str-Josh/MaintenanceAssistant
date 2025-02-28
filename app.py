from flask import Flask, render_template, request, url_for, redirect, session, json
# from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user, AnonymousUserMixin
#user_unauthorized, user_logged_in, user_logged_out
#from flask_login import FlaskLoginClient as LoginClient
# from flask_user import current_user, login_required, roles_required

# from models import db, Users
# from db import db
#from init_db import db
#import flask_migrate as migration
#from .models.user_models import Users

import logging
import os

app = Flask(__name__)
app.config.from_object("config")

logging.basicConfig(filename='errors.log', level=logging.DEBUG)
login_manager = LoginManager()
login_manager.init_app(app)

from mymodels import db, User
db.init_app(app)

with app.app_context():
    db.create_all()

class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = "Guest"

login_manager.anonymous_user = Anonymous

class LoginUser(UserMixin):
    @property
    def is_admin(self):
        return self.is_authenticated and self.id == 'admin'
    
    @property
    def role(self):
        return getattr(self, "_role", None)

    @role.setter
    def role(self, role):
        self._role = role


@login_manager.user_loader
def user_loader(username):
    user_model = User.query.filter_by(username=username).first()
    if user_model is None:
        return None
    user = LoginUser()
    user.username = username
    user.role = user_model.role
    return user


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(
            username = request.form.get("username"),
            password = request.form.get("password"),
            first_name = request.form.get("firstname"),
            last_name = request.form.get("lastname"),
            role = request.form.get("user_role"),
        )

        db.session.add(user)
        try:
            db.session.commit()
        except:
            app.logger.error("User already exists.")
            return redirect(url_for('register'))
        
        app.logger.info("A new user was registered!")
        return redirect(url_for('login'))
    return render_template('forms/sign_up.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username = request.form.get("username")).first()
        
        if user and user.check_password(request.form.get("password")):  # user.password == request.form.get("password"):
            luser = LoginUser()
            luser.id = user.username
            remember = None
            if request.form.get("rememberMe") == "on":
                remember = True
            if login_user(luser, remember=remember):
                return redirect(url_for("home"))
            else:
                return "Bad"
        else:
            app.logger.info("The user gave a bad password")
            return render_template("index.html", pswd_fail=str(True))

    app.logger.info("The request method for login function was GET")
    return render_template("index.html")


@app.route("/logout")
def logout():
    logout_user()
    app.logger.info("A user was logged out.")
    return redirect(url_for("home"))


@app.route("/")
def home():
    if current_user.is_authenticated:
        if current_user.username != "Guest":
            role = current_user.role
            if role == 'admin':
                return render_template("pages/DepartmentHome.html")
            elif role == 'director':
                return None
            elif role == 'manager':
                return None
            elif role == 'staff':
                return None
            else:
                # This is actually an error.
                return render_template("tests/main.html", role=role)
    else:
        app.logger.info("No user is authenticated. Using 'Guest' as username.")
        return render_template("index.html")

@app.route("/team-manager")
@login_required
def team_manager():
    return None

@app.route("/asset-information")
@login_required
def asset_information():
    return None

@app.route("/schedule-manager")
@login_required
def schedule_manager():
    return None


#----------------------------------------------------------------------------#
# Error Handlers.
#----------------------------------------------------------------------------#


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html")

# @app.errorhandler(500)
# def internal_server_error(e):
#     response = e.get_response()
#     response.data = json.dumps({
#         "code": e.code,
#         "name": e.name,
#         "description": e.description,
#     })
#     response.content_type = "application/json"
#     return response


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route("/admin_dashboard")
@login_required
def admin_dashboard():
    return render_template("pages/DepartmentHome.html")

@app.route("/send-request")
@login_required
def send_request():
    app.logger.info("*******We hit the function buddy!!!")
    # return redirect(url_for('main_page'))
    return render_template("pages/sendrequest.html")

@app.route("/update-asset-usage")
@login_required
def update_usage():
    return render_template("pages/updateusage.html")

@app.route("/view-assets")
@login_required
def view_assets():
    return render_template("pages/viewdevices.html")

@app.route("/report-equipment-failure")
@login_required
def equipment_failure_report():
    return render_template("pages/reportbreak.html")

@app.route("/asset-details")
@login_required
def asset_details():
    return render_template("pages/devicedetail.html")

@app.route("/user/<username>", methods=["GET"])
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template("user_profile.html", user=user)
    else:
        return f"User {username} could not be found"
    # if user:
    #     return f"Welcome to {username}'s profile page."
    # else:
    #     return f"User {username} could not be found.", 404


#----------------------------------------------------------------------------#
# Launch Application.
#----------------------------------------------------------------------------#


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8000))
    blueprint.run(host="0.0.0.0", port=port)

