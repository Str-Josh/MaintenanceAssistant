"""
Team:  3
Members: Joshua, Christian, Nick, Elizabeth
Class: CS 483
Proj. Name: Maintenance Assistant
"""


from flask import Flask, render_template, request, url_for, redirect, session, json
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user, AnonymousUserMixin

import datetime as dt
import logging
import os

from mymodels import db, User, Messages, Asset
import failure_model as f_model
from mock_hospital import mock_users, mock_notifications, mock_assets

# PORT = 8000  # Uncomment for Christian.
# PORT = 6000  # Uncomment for Elizabeth.
# PORT = 7000  # Uncomment for Nick.
PORT = 5000  # Uncomment for Josh.
RESET_DB = False  # Do not change unless you want to recreate the entire database.
USE_MOCK_DB = True
DEMONSTRATION = False  # Will enable using 2FA and CAPTCHA when True


app = Flask(__name__)
app.config.from_object("config")


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
logging.basicConfig(filename="errors.log", level=logging.DEBUG)
login_manager = LoginManager()
login_manager.init_app(app)

db.init_app(app)


#----------------------------------------------------------------------------#
# Database Setup.
#----------------------------------------------------------------------------#


def create_mock_db():
    for _mock_user in mock_users:
        _user = User(
            username = _mock_user["username"],
            password = _mock_user["password"],
            first_name = _mock_user["first_name"],
            last_name = _mock_user["last_name"],
            user_role = _mock_user["role"],
        )
        db.session.add(_user)
        db.session.commit()
    for _mock_notification in mock_notifications:
        _notification = Messages(
            sender = _mock_notification["sender"],
            recipient = _mock_notification["recipient"],
            notification_send_date = _mock_notification["notification_send_date"],
            notification_head = _mock_notification["notification_head"],
            notification_body = _mock_notification["notification_body"],
        )
        db.session.add(_notification)
        db.session.commit()
    for _mock_asset in mock_assets:
        _asset = Asset(
            serial_number = _mock_asset["serial_number"],
            device_name = _mock_asset["device_name"],
            brand = _mock_asset["brand"],
            generic_name = _mock_asset["generic_name"],
            manufacturer = _mock_asset["manufacturer"],
            department_location = _mock_asset["department_location"],
            average_use_per_year = _mock_asset["average_use_per_year"],
            total_units_in_service = _mock_asset["total_units_in_service"],
            failure_incidents_in_past_year = _mock_asset["failure_incidents_in_past_year"],
            total_failures_in_history = _mock_asset["total_failures_in_history"],
            last_maintenance_date = _mock_asset["last_maintenance_date"],
            total_maintenance_activities_in_past_year = _mock_asset["total_maintenance_activities_in_past_year"],
            maintenance_type = _mock_asset["maintenance_type"],
            cost_per_maintenance_activity = _mock_asset["cost_per_maintenance_activity"],
            total_maintenance_costs_in_past_year = _mock_asset["total_maintenance_costs_in_past_year"],
            upcoming_maintenance_action_date = _mock_asset["upcoming_maintenance_action_date"],
        )
        db.session.add(_asset)
        db.session.commit()

# with app.app_context():
#     if RESET_DB and not USE_MOCK_DB:
#         db.drop_all()
#         db.create_all()
#     elif RESET_DB and USE_MOCK_DB:
#         db.drop_all()
#         db.create_all()
#         create_mock_db()
#     else:
#         db.create_all()


#----------------------------------------------------------------------------#
# User Authorization.
#----------------------------------------------------------------------------#


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
    user.role = user_model.user_role
    return user


#----------------------------------------------------------------------------#
# Home Page.
#----------------------------------------------------------------------------#


@app.route("/")
def home():
    if current_user.is_authenticated:
        if current_user.username != "Guest":
            role = current_user.role
            if role == 'admin':
                return render_template("pages/Director/DirectorHome.html")
            elif role == 'director':
                return render_template("pages/Director/DirectorHome.html")
            elif role == 'manager':
                # Backend stuff for viewing devices needing upcoming repairs.
                company_assets = Asset.query.all()
                maintenance_required = []
                date_span_interval = 19  # number of days to span the interval
                upcoming_maintenance_actions_datespan = dt.date.today() + dt.timedelta(days=date_span_interval)

                for _asset in company_assets:
                    if _asset.upcoming_maintenance_action_date:
                        if _asset.upcoming_maintenance_action_date <= upcoming_maintenance_actions_datespan:
                            instance = {
                                "serial_number": _asset.asset_id,  # TODO: need to change to actual serial number from DB (I don't feel like updating mock DB rn sorry)
                                "repair_by": _asset.upcoming_maintenance_action_date,
                                "department_location": _asset.department_location
                            }  # dictionary of the important values 
                            maintenance_required.append(instance)

                # Backend stuff for notifications bar.
                notifications = Messages.query.filter_by(recipient=current_user.username).all()

                return render_template("pages/Manager/ManagerHome.html", assets=maintenance_required, notifications=notifications)
            elif role == 'staff':
                return None
            else:
                return redirect(url_for("unauthorized"))
    else:
        app.logger.info("An unauthorized user directed to '/'. Requesting login credentials.")
        return render_template("forms/Login.html")


#----------------------------------------------------------------------------#
# Supporting Pages For Login.
#----------------------------------------------------------------------------#

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        role = request.form.get("user_role").lower()
        if " " in role:
            role = role.split(" ")[1]
        
        user = User(
            username = request.form.get("username"),
            password = request.form.get("password"),
            first_name = request.form.get("firstname"),
            last_name = request.form.get("lastname"),
            user_role = role,
        )

        db.session.add(user)
        try:
            db.session.commit()
        except:
            app.logger.error("User already exists.")
            return redirect(url_for('register'))
        
        app.logger.info("A new user was registered!")
        return redirect(url_for('login'))
    # return render_template('forms/sign_up.html')
    return redirect(url_for("home"))

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
                app.config['REMEMBER_COOKIE_DURATION'] = dt.timedelta(days=1)
            if login_user(luser, remember=remember):
                return redirect(url_for("home"))
            else:
                return "Bad"
        else:
            app.logger.info("The user gave a bad password")
            return render_template("forms/Login.html", pswd_fail=str(True))

    app.logger.info("The request method for login function was GET")
    return render_template("forms/Login.html")


@app.route("/logout")
def logout():
    logout_user()
    app.logger.info("A user was logged out.")
    return redirect(url_for("home"))


#----------------------------------------------------------------------------#
# Dashboards For User Roles.
#----------------------------------------------------------------------------#


@app.route("/director-dashboard")
@login_required
def director_dashboard():
    return render_template("pages/Director/DirectorHome.html")


#----------------------------------------------------------------------------#
# Maybe Make Use.
#----------------------------------------------------------------------------#


@app.route("/team-manager")
@login_required
def team_manager():
    return None

@app.route("/asset-information")
@login_required
def asset_information():
    return None


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route("/send-request", methods=["POST", "GET"])
@login_required
def send_request():
    if request.method == "POST":
        maintenance_managers = User.query.filter_by(user_role="manager")

        urgencyLevel = request.form.get("urgencyCheck")  # TODO: Implement this in DB.
        machineNeedingMaint = request.form.get("subject")
        subject = "Maintenance Request: " + machineNeedingMaint
        body = request.form.get("message")
        today = dt.date.today()
        # If urgent, elevate immediately
        if urgencyLevel == "urgent":
            # Elevate to managers immediately
            pass

        for _ in maintenance_managers:
            notification = Messages(
                sender = current_user.username,
                recipient = _.username,
                notification_send_date = today,
                notification_head = subject,
                notification_body = body,
                # status = "initial-notice"
            )

            db.session.add(notification)
            db.session.commit()
            app.logger.info(f"We have added Messages to db for {_.username}.")
        return render_template("pages/PublicAccess/SendMaintenanceRequest.html", success_message="Notice Submitted!")
    return render_template("pages/PublicAccess/SendMaintenanceRequest.html")


@app.route("/update-asset-usage", methods=["POST", "GET"])
@login_required
def update_usage():
    if request.method == "POST":
        ## Do our updating the usage bs
        return render_template("pages/Director/UpdateDeviceUsage.html", success_message="Usage has been updated!")
    return render_template("pages/Director/UpdateDeviceUsage.html")


@app.route("/asset-manager", methods=["POST", "GET"])
@login_required
def asset_manager():
    if request.method == "POST":
        return None
    return render_template("pages/Director/AssetManager.html")


@app.route("/view-assets", methods=["GET"])
@login_required
def view_assets():
    return render_template("pages/Director/AssetManagement/ViewAssets.html")


@app.route("/assign_device")
def assign_device(original_page):
    return redirect(original_page + ".html")


@app.route("/add-asset", methods=["POST", "GET"])
@login_required
def add_asset():
    if request.method == "POST":
        if request.is_json:
            # first half of page.
            device_name = request.form.get("deviceName")
            brand_name = request.form.get("brandName")
            generic_name = request.form.get("genName")
            manufacturer_name = request.form.get("manName")
            stored_department = request.form.get("homeDepLoc")
            installation_date = request.form.get("instDate")
            average_uses_py = request.form.get("avgUseYear")

            # second half
            data = request.get_json()  # this should be the handsontable data.

            asset = Asset(
                device_name = device_name,
            )
            # try:
            db.commit(asset)
            # except:

            # Calculate expectaction for next repair
            # f_model.kaplan_meier_estimator_function()

            app.logger.info(data)
            return redirect(url_for("add_asset"))
    return render_template("pages/Director/AssetManagement/AddNewDevice.html")


# @app.route("/asset-details")
# @login_required
# def asset_details():
#     return render_template("pages/devicedetail.html")


@app.route("/schedule-repair", methods=["GET", "POST"])
@login_required
def schedule_repair(repair_by_date):
    if request.method == "POST":
        return None
    return render_template("")

@app.route("/asset-details/<serial_number>", methods=["GET", "POST"])
@login_required
def asset_details(serial_number):
    if current_user.user_role != "director" or current_user.user_role != "manager" or not current_user.is_authenticated:
        redirect(url_for("unauthorized"))
    if request.method == "POST":
        return None
    return render_template("pages/PublicAcess/AssetDetails.html", asset_id=serial_number)

#----------------------------------------------------------------------------#
# Manager Home Routes.
#----------------------------------------------------------------------------#

@app.route("/notif-rud")
@login_required
def notification_crud_without_c(id, operation):
    if operation == "remove":
        return None
    elif operation == "elevate":
        return None
    elif operation == "assignSelf":
        return None
    return None

@app.route("/delete-notification")
@login_required
def delete_notification(id):
    notification_to_delete = Messages.query.get(id)
    if notification_to_delete:
        db.session.delete(notification_to_delete)
        db.session.commit()
        return f"Messages has successfully been removed.", 200
    else:
        return f"Messages was not found.", 404
    
@app.route("/elevate")
@login_required
def elevate(id):
    return None


#----------------------------------------------------------------------------#
# Stretch Goals.
#----------------------------------------------------------------------------#


@app.route("/user/<username>", methods=["GET"])
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template("pages/PublicAccess/user_profile.html", user=user)
    else:
        return f"User {username} could not be found"
    

#----------------------------------------------------------------------------#
# Error Handlers.
#----------------------------------------------------------------------------#


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html")


#----------------------------------------------------------------------------#
# Launch Application.
#----------------------------------------------------------------------------#


if __name__ == "__main__":
    #port = int(os.environ.get("PORT", 10000))
    #app.run(host="0.0.0.0", port=port)
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
