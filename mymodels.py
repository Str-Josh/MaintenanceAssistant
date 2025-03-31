from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
import datetime as dt

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    first_name = db.Column(db.String(25), nullable=True)
    last_name = db.Column(db.String(25), nullable=True)
    role = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(25), nullable=False)

    def check_password(self, password):
        return sha256_crypt.verify(password, self.password)
    
    def __init__(self, username, first_name, last_name, role, password):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.password = sha256_crypt.encrypt(password)

class Role(UserMixin, db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(25), nullable=False)

    def define_permissions(self):
        self.create_new_users = False
        self.access_asset_info = False
        self.access_team_info = False
        self.update_teams_schedules = False

class Notification(db.Model):
    notification_id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(25), nullable=False)
    recipient = db.Column(db.String(25), nullable=False)
    notification_send_date = db.Column(db.Date, nullable=False)
    notification_head = db.Column(db.String(35), nullable=False)
    notification_body = db.Column(db.String(160), nullable=True)
    #status = db.Column(db.String(), nullable=False)

class Asset(db.Model):
    asset_id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.Integer, nullable=False)
    device_name = db.Column(db.String(40), nullable=False)
    brand = db.Column(db.String(40), nullable=False)
    generic_name = db.Column(db.String(50), nullable=False)
    manufacturer = db.Column(db.String(40), nullable=False)
    department_location = db.Column(db.String(40), nullable=True)
    
    # Historical Usage Data
    # average_use_per_year = db.Column(db.Integer, nullable=False)
    average_use_per_year = db.Column(db.String(40), nullable=False)
    total_units_in_service = db.Column(db.Integer, nullable=False)

    # Historical Failure Data
    failure_incidents_in_past_year = db.Column(db.Integer, nullable=False)
    total_failures_in_history = db.Column(db.Integer, nullable=False)

    # Maintenace Log Data
    last_maintenance_date = db.Column(db.Date, nullable=False)
    total_maintenance_activities_in_past_year = db.Column(db.Integer, nullable=False)
    maintenance_type = db.Column(db.String(60), nullable=True)
    cost_per_maintenance_activity = db.Column(db.Numeric(10, 2), nullable=True)
    total_maintenance_costs_in_past_year = db.Column(db.Numeric(10, 2), nullable=True)
    #usage_data = db.Column(db.Text)
    #failure_data = db.Column()
    #maintenance_log_data = db.Column()

    upcoming_maintenance_action_date = db.Column(db.Date, nullable=True)

    def classify_upcoming_maintenance_action(self):
        if 1:
            pass
        pass

class MaintenanceTeam(db.Model):
    maintenance_team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(30), unique=True, nullable=False)
    # team_creation_date = db.Column(db.DateTime(default=dt.datetime.utcnow()))
    # team_creation_date = db.Column(db.DateTime(default=dt.timezone.utc()))

class MaintenanceStaff(db.Model):
    staff_id = db.Column(db.Integer, primary_key=True)
