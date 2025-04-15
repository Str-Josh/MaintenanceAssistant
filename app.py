"""
Team:  3
Members: Joshua, Christian, Nick, Elizabeth
Class: CS 483
Proj. Name: Maintenance Assistant
"""


from flask import Flask, render_template, request, url_for, redirect, session, json
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user, AnonymousUserMixin
from werkzeug.exceptions import NotFound

import datetime as dt
import logging
import os

from mymodels import db, User, Messages, Asset
import failure_model as f_model
from mock_hospital import mock_users, mock_notifications, mock_assets
from utils import RegistrationForm, RegisterAssetForm, TeamMemberSendMessage, SearchAssetForm

PORT = 5000  # Uncomment for Josh.
RESET_DB = False  # Do not change unless you want to recreate the entire database.
USE_MOCK_DB = False  # Just in case...
DEMONSTRATION = False  # Will enable using 2FA and CAPTCHA when True


app = Flask(__name__)
app.config.from_object("config")


# Server-hosted
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logging.basicConfig(filename="errors.log", level=logging.DEBUG)
login_manager = LoginManager()
login_manager.init_app(app)

db.init_app(app)


#----------------------------------------------------------------------------#
# Database Setup.
#----------------------------------------------------------------------------#

# Don't want it to error out... I know it will :'(
# def create_mock_db():
#     for _mock_user in mock_users:
#         _user = User(
#             username = _mock_user["username"],
#             password = _mock_user["password"],
#             first_name = _mock_user["first_name"],
#             last_name = _mock_user["last_name"],
#             user_role = _mock_user["role"],
#         )
#         db.session.add(_user)
#         db.session.commit()
#     for _mock_notification in mock_notifications:
#         _notification = Messages(
#             sender = _mock_notification["sender"],
#             recipient = _mock_notification["recipient"],
#             notification_send_date = _mock_notification["notification_send_date"],
#             notification_head = _mock_notification["notification_head"],
#             notification_body = _mock_notification["notification_body"],
#         )
#         db.session.add(_notification)
#         db.session.commit()
#     for _mock_asset in mock_assets:
#         _asset = Asset(
#             serial_number = _mock_asset["serial_number"],
#             device_name = _mock_asset["device_name"],
#             brand = _mock_asset["brand"],
#             generic_name = _mock_asset["generic_name"],
#             manufacturer = _mock_asset["manufacturer"],
#             department_location = _mock_asset["department_location"],
#             average_use_per_year = _mock_asset["average_use_per_year"],
#             total_units_in_service = _mock_asset["total_units_in_service"],
#             failure_incidents_in_past_year = _mock_asset["failure_incidents_in_past_year"],
#             total_failures_in_history = _mock_asset["total_failures_in_history"],
#             last_maintenance_date = _mock_asset["last_maintenance_date"],
#             total_maintenance_activities_in_past_year = _mock_asset["total_maintenance_activities_in_past_year"],
#             maintenance_type = _mock_asset["maintenance_type"],
#             cost_per_maintenance_activity = _mock_asset["cost_per_maintenance_activity"],
#             total_maintenance_costs_in_past_year = _mock_asset["total_maintenance_costs_in_past_year"],
#             upcoming_maintenance_action_date = _mock_asset["upcoming_maintenance_action_date"],
#         )
#         db.session.add(_asset)
#         db.session.commit()

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
                                "asset_id": _asset.asset_id,  # TODO: need to change to actual serial number from DB (I don't feel like updating mock DB rn sorry)
                                "repair_by": _asset.upcoming_maintenance_action_date,
                                "department_location": _asset.location
                            }  # dictionary of the important values 
                            maintenance_required.append(instance)

                # Backend stuff for notifications bar.
                notifications = Messages.query.filter_by(recipient=current_user.username).all()

                return render_template("pages/Manager/ManagerHome.html", assets=maintenance_required, notifications=notifications)
            elif role == 'staff':
                this_user = User.query.filter_by(username = current_user.username)
                assets = Asset.query.all()
                for _asset in assets:
                    # if _asset.scheduled_date
                    pass
                return render_template("pages/Staff/StaffHome.html")
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
    form = RegistrationForm(request.form)
    app.logger.info(form.data)
    app.logger.info(form.errors)
    app.logger.info(form.form_errors)
    if request.method == "POST" and form.validate():
        app.logger.info(form.data)
        role = request.form.get("user_role").lower()
        if " " in role:
            role = role.split(" ")[1]
        
        user = User(
            username = form.username.data,
            password = form.password.data,
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            user_role = role,
            email = form.email.data,
        )

        # Below is old version for safe keeping.
        # user = User(
        #     username = request.form.get("username"),
        #     password = request.form.get("password"),
        #     first_name = request.form.get("firstname"),
        #     last_name = request.form.get("lastname"),
        #     user_role = role,
        #     email = request.form.get("email"),
        # )

        db.session.add(user)
        try:
            db.session.commit()
            app.logger.info("A new user has been added to the database.")
        except:
            app.logger.error("User already exists.")
            return render_template("forms/sign_up.html", form=form)
            # return render_template("forms/sign_up.html", validators_response=form.errors)
            return redirect(url_for('register'))
        
        app.logger.info("A new user was registered!")
        return redirect(url_for('home'))
    elif request.method != "POST":
        return render_template("forms/sign_up.html", form=form)
    else:
        # app.logger.error(form.errors)
        return render_template("forms/sign_up.html", form=form)
        # return render_template("forms/sign_up.html", validators_response=form.errors)
        # return render_template("forms/sign_up.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username = request.form.get("username")).first()
        
        if user and user.check_password(request.form.get("password")):  # user.password == request.form.get("password"):
            luser = LoginUser()
            luser.id = user.username
            remember = None
            if request.form.get("rememberMe") == "on":
                # set the remember me cookie to a single day
                remember = True
                app.config['REMEMBER_COOKIE_DURATION'] = dt.timedelta(days=1)
            if login_user(luser, remember=remember):
                return redirect(url_for("home"))
            else:
                # if user login is not accepted, following occurs
                return "Bad"
        elif user:
            app.logger.warning("The user doesn't exist")
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


@app.route("/reset-password")
def reset_password(source):
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        # Send a request to admin but it must require that you already have content in the form
        # for _ in maintenance_managers:
        #     notification = Messages(
        #         sender = current_user.username,
        #         recipient = _.username,
        #         notification_send_date = today,
        #         notification_head = subject,
        #         notification_body = body,
        #         # status = "initial-notice"
        #     )

        #     db.session.add(notification)
        #     db.session.commit()
        #     app.logger.info(f"Added Messages to db for {_.username}.")

        # managers = Users.query.
        # for _ in 
        # reset_password_request = Messages(
        #     sender = form.first_name + " " + form.last_name,
        #     # recipient = _.user_name,
        #     notification_send_date = 9,
        #     notification_head = 0,
        #     notification_bdoy = 0,
        # )
        return None
    elif request.method != "POST":
        return None
    else:
        return render_template(source, validators_response=form.errors)


#----------------------------------------------------------------------------#
# Dashboards For User Roles.
#----------------------------------------------------------------------------#


@app.route("/director-dashboard")
@login_required
def director_dashboard():
    return render_template("pages/Director/DirectorHome.html")


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
        if urgencyLevel.lower() == "urgent":
            # Elevate to managers immediately
            # client = Client(account_sid, auth_token)
            # message = client.messages.create(to="")
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
            app.logger.info(f"Added Messages to db for {_.username}.")
        return render_template("pages/PublicAccess/SendMaintenanceRequest.html", success_message="Notice Submitted!")
    return render_template("pages/PublicAccess/SendMaintenanceRequest.html")


@app.route("/update-asset-usage", methods=["POST", "GET"])
@login_required
def update_usage():
    if request.method == "POST":
        ## Do our updating the usage bs
        return render_template("pages/Director/UpdateDeviceUsage.html", success_message="Usage has been updated!")
    return render_template("pages/Director/UpdateDeviceUsage.html")


# Do we still need this??
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


# I don't remember what this was for ngl...
@app.route("/assign_device")
def assign_device(original_page):
    return redirect(original_page + ".html")


@app.route("/search-asset", methods=["GET", "POST"])
@login_required
def search_asset():  # maybe change to generic_name? idek
    form = SearchAssetForm(request.form)

    if request.method == "POST" and form.validate():        
        search_by = form.search_by.data
        search_phrase = form.search_phrase.data

        found_assets = Asset.query.filter(
            getattr(Asset, search_by).ilike(f"%{search_phrase}%")
        ).all()

        if not found_assets:
            return render_template(
                "pages/Director/AssetManagement/SearchAssets.html",
                form=form,
                no_assets_found="True"
            )

        app.logger.info(f"We found some assets:\n{found_assets}")

        return render_template(
            "pages/Director/AssetManagement/SearchAssets.html",
            form=form,
            found_assets=found_assets,
        )
    elif request.method != "POST":
        return render_template("pages/Director/AssetManagement/SearchAssets.html", form=form)
    else:
        return render_template("pages/Director/AssetManagement/SearchAssets.html", form=form)


@app.route("/add-asset", methods=["POST", "GET"])
@login_required
def add_asset():
    form = RegisterAssetForm(request.form)
    if request.method == "POST" and form.validate():
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
            app.logger.info(data)  # wtf is even in here...?

            # installation_date & generic_name workaround :)
            description = generic_name + ";" + installation_date
            # this will always be okay since brand_name max length = 

            # 0 means it's nullable, 1 means it's not
            asset = Asset(
                device_name = device_name,
                brand = brand_name,  # brand_name = brand_name,
                # generic_name = generic_name,
                manufacturer_name = manufacturer_name,  # manufacturer_name = manufacturer_name,
                stored_department = stored_department,
                # installation_date = installation_date,
                description = description,  # :)
                image_path = 0,

                serial_number = 1,
                generic_name = 1,
                average_uses_py = average_uses_py,
                total_units_in_service = 1,

                failure_incidents_in_past_year = 1,
                total_failures_in_history = 1,

                last_maintenance_date = 1,
                total_maintenance_activities_in_past_year = 1,
                maintenance_type = 0,
                cost_per_maintenance_activity = 0,
                total_maintenance_costs_in_past_year = 0,
                upcoming_maintenance_action_date = 0
            )
            db.session.add(asset)
            try:
                db.commit(asset)
            except:
                app.logger.info("Asset already exists")

            # Calculate expectaction for next repair
            # f_model.kaplan_meier_estimator_function()

            app.logger.info(data)
            # return redirect(url_for("add_asset"))
            return render_template(url_for("home"))
    elif request.method != "POST":
        return render_template("pages/Director/AssetManagement/AddNewDevice.html", form=form)
    else:
        # occurs when form validation errors arise
        return render_template("pages/Director/AssetManagement/AddNewDevice.html", form=form)


@app.route("/asset-details/<serial_number>", methods=["GET", "POST"])
@login_required
def asset_details(serial_number):
    if current_user.role not in ["director", "manager"]:
        return redirect(url_for("unauthorized"))

    asset = Asset.query.get(serial_number)
    if not asset:
        return "Asset not found", 404

    return render_template("pages/PublicAccess/AssetDetails.html", asset=asset)


@app.route("/schedule-repair", methods=["GET", "POST"])
@login_required
def schedule_repair(repair_by_date):
    if request.method == "POST":
        return None
    return render_template("")


@app.route("/message-team-members/<role>", methods=["GET", "POST"])
@login_required
def message_team_members(role):
    form = TeamMemberSendMessage(request.form)
    acceptable_roles = ["director", "manager", "staff"]
    if role not in acceptable_roles:
        raise NotFound("The requested team member role was unrecognized.")

    role_specific_members = User.query.filter_by(user_role=role)
    form.recipient_member.choices = [ (user.first_name, user.first_name) for user in role_specific_members.all() ]

    if form.validate_on_submit():
        _member = form.recipient_member.data
        _subject = form.message_subject.data
        _body = form.message_body.data

        new_message = Messages(
            sender = current_user.username,
            recipient = _member,
            notification_send_date = dt.date.today(),
            notification_head = _subject,
            notification_body = _body,
        )
        return redirect(url_for("message_team_members", member_role=role))

    return render_template(
        "pages/PublicAccess/MessageTeamMembers.html", 
        form=form, 
        member_role=role
    )


@app.route("/upload-upcoming")
@login_required
def upload_upcoming():
    return None


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
    return render_template("errors/404.html", error_message=e.description), 404


#----------------------------------------------------------------------------#
# Launch Application.
#----------------------------------------------------------------------------#


if __name__ == "__main__":
    # port = int(os.environ.get("PORT", 10000))
    # app.run(host="0.0.0.0", port=port)
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
