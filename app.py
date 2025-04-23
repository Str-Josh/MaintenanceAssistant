"""
Team:  3
Members: Joshua, Christian, Nick, Elizabeth
Class: CS 483
Proj. Name: Maintenance Assistant
"""


from flask import Flask, render_template, make_response, request, url_for, redirect, session, json
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user, AnonymousUserMixin
from flask_caching import Cache, CachedResponse
from werkzeug.exceptions import NotFound
from rest_api import MaintenanceAssistantAPI

import datetime as dt
import logging
import os
import urllib

from mymodels import db, User, Messages, Asset, Activity, ActivityAssetUser
import failure_model as f_model
# from mock_hospital import mock_users, mock_notifications, mock_assets
from mock_hospital import *
from env_settings_admin import EnvironmentSettings
# from utils import RegistrationForm, RegisterAssetForm, TeamMemberSendMessage, ReplyMemberMessage, SearchAssetForm\
from utils import *

PORT = 5000
RESET_DB = False  # Do not change unless you want to recreate the entire database.
USE_MOCK_DB = True  # Just in case...
DEMONSTRATION = False  # Will enable using 2FA and CAPTCHA when True
# LOCAL = True  # Since I prefer to test locally before pushing. Just need to add DB URI.


app = Flask(__name__)
app.config.from_object("config")
cache = Cache(app)

ENV_SETTINGS = EnvironmentSettings.settings

# Server-hosted
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logging.basicConfig(filename="errors.log", level=logging.DEBUG)
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.init_app(app)

db.init_app(app)
api = MaintenanceAssistantAPI(db=db)


#----------------------------------------------------------------------------#
# Database Setup.
#----------------------------------------------------------------------------#


def create_mock_db():
    api.add_row(User, mock_users, multiple_addition=True)
    api.add_row(Messages, mock_notifications, multiple_addition=True)
    api.add_row(Asset, mock_assets, multiple_addition=True)
    api.add_row(Activity, mock_activities, multiple_addition=True)
    api.add_row(ActivityAssetUser, mock_activitiesUsers, multiple_addition=True)

# if LOCAL:
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
    user.id = user_model.user_id
    user.role = user_model.user_role
    return user


#----------------------------------------------------------------------------#
# Home Page.
#----------------------------------------------------------------------------#


@app.route("/")
# @cache.cached(query_string=True)
def home():
    if current_user.is_authenticated:
        if current_user.username != "Guest":
            role = current_user.role
            if role == 'admin':
                # return CachedResponse(response=make_response(render_template("pages/Director/DirectorHome.html"), timeout=20))
                return render_template("pages/Director/DirectorHome.html")
            elif role == 'director':
                # return CachedResponse(response=make_response(render_template("pages/Director/DirectorHome.html", timeout=20)))
                return render_template("pages/Director/DirectorHome.html")
            elif role == 'manager':
                # Backend stuff for viewing devices needing upcoming repairs.
                company_assets = Asset.query.all()
                maintenance_required = []
                date_span_interval = ENV_SETTINGS["Upcoming-Maintenance-Date-Span"]  # number of days to span the interval
                upcoming_maintenance_actions_datespan = dt.date.today() + dt.timedelta(days=date_span_interval)

                for _asset in company_assets:
                    if _asset.upcoming_maintenance_action_date:
                        if _asset.upcoming_maintenance_action_date <= upcoming_maintenance_actions_datespan:
                            instance = {
                                "asset_id": _asset.asset_id,  # TODO: need to change to actual serial number from DB (I don't feel like updating mock DB rn sorry)
                                "repair_by": _asset.upcoming_maintenance_action_date,
                                "department_location": _asset.location,
                                "serial_number": _asset.serial_number,
                            }  # dictionary of the important values 
                            maintenance_required.append(instance)

                # Backend stuff for notifications bar.
                notifications = Messages.query.filter_by(recipient=current_user.username).all()
                app.logger.warning(maintenance_required)

                return render_template("pages/Manager/ManagerHome.html", assets=maintenance_required, notifications=notifications)
                # return CachedResponse(
                #     response=make_response(
                #         render_template(
                #             "pages/Manager/ManagerHome.html", 
                #             assets=maintenance_required, notifications=notifications
                #         )
                #     ),
                #     timeout=10
                # )
            elif role == 'staff':
                activityAssetUserInstances = ActivityAssetUser.query.filter_by(user_id = current_user.id).all()
                assignments = []
                # app.logger.error(f"Act Ass Use:  \n{activityAssetUserInstances}\n\n")
                for _activityAssetUser in activityAssetUserInstances:
                    ## grabbing other things from activitiesAssetUsers
                    assignments.append(
                        [
                            ## Wanna add the things but this is easier than implementing a bunch of join stuff imo
                            User.query.filter_by(user_id = _activityAssetUser.user_id).first(),
                            Asset.query.filter_by(asset_id = _activityAssetUser.asset_id).first(),
                            Activity.query.filter_by(activity_id = _activityAssetUser.activity_id).first(),
                            _activityAssetUser
                        ]
                    )
                app.logger.info(f"assignments structure:\n{assignments}\n\n")
                return render_template("pages/Staff/StaffHome.html", assignments=assignments)
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
        db.session.add(user)
        try:
            db.session.commit()
            app.logger.info("A new user has been added to the database.")
        except:
            app.logger.error("User already exists.")
            return render_template("forms/sign_up.html", form=form)
        
        app.logger.info("A new user was registered!")
        return redirect(url_for('home'))
    elif request.method != "POST":
        return render_template("forms/sign_up.html", form=form)
    else:
        return render_template("forms/sign_up.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username = request.form.get("username")).first()
        
        if user and user.check_password(request.form.get("password")):
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
    form = SendRequestForm(request.form)
    if request.method == "POST":
        maintenance_managers = User.query.filter_by(user_role="manager")

        generic_name = form.generic_name.data
        detailed_message = form.detailed_message.data

        subject = "Maintenance Request: " + generic_name
        today = dt.date.today()

        # If urgent, elevate immediately
        if form.urgency_level.data.lower() == "urgent":
            # Elevate to managers immediately
            # client = Client(account_sid, auth_token)
            # message = client.messages.create(to="")
            pass

        notificationInstances = []
        for manager in maintenance_managers:
            notificationInstances.append(
                {
                    "sender": current_user.username,
                    "recipient": manager.username,
                    "notification_send_date": today,
                    "notification_head": subject,
                    "notification_body": detailed_message,
                },
            )
            app.logger.info(f"Adding a message to db for {manager.username}.")
        api.add_row(Messages, multiple_addition=True, data=notificationInstances)

        form.generic_name.data = ""
        form.detailed_message.data = ""
        return render_template(
            "pages/PublicAccess/SendMaintenanceRequest.html", 
            success_message="Notice Submitted!",
            form=form,
        )

    return render_template(
        "pages/PublicAccess/SendMaintenanceRequest.html",
        form=form,
    )


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

    # asset = Asset.query.get(serial_number)
    asset = Asset.query.filter_by(serial_number=serial_number).first()
    app.logger.error(asset)
    if not asset:
        return "Asset not found", 404

    return render_template("pages/PublicAccess/AssetDetails.html", asset=asset)


@app.route("/schedule-repair", methods=["GET", "POST"])
@login_required
def schedule_repair(repair_by_date):
    if request.method == "POST":
        return "haha, you thought I implemented this??? HAHAHAHA"
    return "haha, you thought I implemented this??? HAHAHAHA"
    # return render_template("")


@app.route("/message-team-members/<role>", methods=["GET", "POST"])
@login_required
def message_team_members(role):
    form = TeamMemberSendMessage(request.form)
    role_specific_members = User.query.filter_by(user_role=role)
    form.recipient_member.choices = [ (user.first_name, user.first_name) for user in role_specific_members.all() ]
    if request.method == "POST" and form.validate():
        # acceptable_roles = ["director", "manager", "staff"]
        # if role not in acceptable_roles:
        #     raise NotFound("The requested team member role was unrecognized.")

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
        db.session.add(new_message)
        app.logger.error(new_message)
        db.session.commit()
        # return redirect(url_for("message_team_members", member_role=role))
        return redirect(url_for("home"))

        # if form.validate_on_submit():
        # if form.validate():
        #     _member = form.recipient_member.data
        #     _subject = form.message_subject.data
        #     _body = form.message_body.data

        #     new_message = Messages(
        #         sender = current_user.username,
        #         recipient = _member,
        #         notification_send_date = dt.date.today(),
        #         notification_head = _subject,
        #         notification_body = _body,
        #     )
        #     db.session.add(new_message)
        #     app.logger.error(new_message)
        #     db.session.commit()
        #     # return redirect(url_for("message_team_members", member_role=role))
        #     return redirect(url_for("home"))
        # else:
        #     app.logger.error("What is going on")
    elif not form.validate():
        app.logger.error(form.data)
        app.logger.error(form.errors)
        # return "This is fucked"
        return render_template(
            "pages/PublicAccess/MessageTeamMembers.html", 
            form=form, 
            member_role=role
        )

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


# TODO: Finish this after setting assets as scheduled.
@app.route("/view-upcoming-events")
@login_required
def view_upcoming_events():
    # @cache.cached(timeout=10)
    span = ENV_SETTINGS["Upcoming-Maintenance-Date-Span"]  # set it at 14 days for now.
    upcoming_assets = Asset.query.filter_by(upcoming_maintenance_action_date=span).all()
    app.logger.info(upcoming_assets)

    # return render_template("", upcoming_assets=upcoming_assets)
    return render_template("pages/Staff/UpcomingMaintenanceView.html", upcoming_assets=upcoming_assets)


@app.route("/assign_schedule/<asset_serial_number>/<crud_action>", methods=["GET", "POST"])
@login_required
def assign_schedule(asset_serial_number, crud_action):

    if request.method == "POST":
        
        if crud_action == "create":
            pass
        elif crud_action == "edit":
            pass
        else:
            pass
        return None

    else:
        return None

@app.route("/delete-notification", methods=["POST"])
@login_required
def delete_notification():
    id = request.form.get("id")
    source = request.form.get("source")
    notification_to_delete = Messages.query.filter_by(notification_id=id).first()
    deletion_params = True
    if notification_to_delete:
        db.session.delete(notification_to_delete)
        try:
            db.session.commit()
        except:
            raise Exception("Message does not exist")
        return redirect(url_for("home", delete_params=deletion_params))
    else:
        return f"Messages was not found.", 404


@app.route("/reply/<notification_sender>/<notification_subject>", methods=["POST", "GET"])
@login_required
def reply_notification(notification_sender, notification_subject):
    app.logger.error(f"Accessing: {current_user.username}")
    form = ReplyMemberMessage(request.form)
    
    decoded_subject = urllib.parse.unquote_plus(notification_subject)
    form.message_subject.data = f"RE: {decoded_subject}"
    app.logger.error(f"Accessing: {current_user.username}")
    if request.method == "POST":
        reply = Messages(
            sender = current_user.username,
            recipient = notification_sender,
            notification_send_date = dt.date.today(),
            notification_head = form.message_subject.data,
            notification_body = form.message_body.data,
        )
        db.session.add(reply)
        db.session.commit()
        # return redirect(url_for("home"))
        return render_template(
            "pages/PublicAccess/SendMessagePart.html", 
            form=form, 
            notif_data={
                "sender": notification_sender,
                "subject": decoded_subject,
            }
        )
    return "this is bug. Please report me."


@app.route("/elevate")
@login_required
def elevate(id):
    return None


#----------------------------------------------------------------------------#
# Stretch Goals.
#----------------------------------------------------------------------------#


@app.route("/user/<username>", methods=["GET"])
def user_profile(username):
    user = User.query.all()
    cn = 1
    app.logger.info(user)
    for elem in user:
        app.logger.info("I'm doing something.")
        app.logger.info(elem)
        app.logger.info(elem.username)
        if cn == 2:
            break
        cn = cn + 1
    return f"I'm doing something"
    # user = User.query.filter_by(username=username).first()
    # if user:
    #     return render_template("pages/PublicAccess/user_profile.html", user=user)
    # else:
    #     return f"User {username} could not be found"
    

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
