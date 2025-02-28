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

class MaintenanceTeam(db.Model):
    maintenance_team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(30), unique=True, nullable=False)
    # team_creation_date = db.Column(db.DateTime(default=dt.datetime.utcnow()))
    # team_creation_date = db.Column(db.DateTime(default=dt.timezone.utc()))

class MaintenanceStaff(db.Model):
    staff_id = db.Column(db.Integer, primary_key=True)
