from flask_sqlalchemy import SQLAlchemy
import datetime as dt

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(25), nullable=False)
    first_name = db.Column(db.String(25), nullable=True)
    last_name = db.Column(db.String(25), nullable=True)

class Roles(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(25), nullable=False)

    def define_permissions(self):
        self.create_new_users = False
        self.access_asset_info = False
        self.access_team_info = False
        self.update_teams_schedules = False

class MaintenanceTeam(db.Model):
    maintenance_team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(30), unique=True, nullable=False)
    # team_creation_date = db.Column(db.DateTime(default=dt.datetime.utcnow()))
    # team_creation_date = db.Column(db.DateTime(default=dt.timezone.utc()))

class MaintenanceStaff(db.Model):
    staff_id = db.Column(db.Integer, primary_key=True)
