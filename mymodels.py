
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
import datetime as dt

# Initialize SQLAlchemy
db = SQLAlchemy()

# Association Tables
users_departments = db.Table(
    'Users_Departments',
    db.Column('user_id', db.Integer, db.ForeignKey('Users.user_id'), primary_key=True),
    db.Column('department_id', db.Integer, db.ForeignKey('Departments.department_id'), primary_key=True)
)

user_messages = db.Table(
    'User_Messages',
    db.Column('sender', db.Integer, db.ForeignKey('Users.user_id')),
    db.Column('notification_id', db.Integer, db.ForeignKey('Messages.notification_id')),
    db.Column('recipient', db.Integer, db.ForeignKey('Users.user_id'))
)

class Department(db.Model):
    __tablename__ = 'Departments'
    department_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(255), unique=True, nullable=False)
    user_role = db.Column(db.String(50))
    password_hash = db.Column(db.String(64))

    departments = db.relationship('Department', secondary=users_departments, backref='users')

    def check_password(self, password):
        return sha256_crypt.verify(password, self.password_hash)

    def __init__(self, username, first_name, last_name, email, user_role, password):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.user_role = user_role
        self.password_hash = sha256_crypt.encrypt(password)


class Asset(db.Model):
    __tablename__ = 'Assets'
    
    asset_id = db.Column(db.String(30), primary_key=True)
    asset_name = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    brand = db.Column(db.String(50), nullable=True)
    manufacturer = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    department = db.Column(db.Integer, db.ForeignKey('Departments.department_id'), nullable=True)
    image_path = db.Column(db.String(255), nullable=True)

    serial_number = db.Column(db.Integer, nullable=False)
    generic_name = db.Column(db.String(50), nullable=False)
    average_use_per_year = db.Column(db.String(40), nullable=False)
    total_units_in_service = db.Column(db.Integer, nullable=False)

    failure_incidents_in_past_year = db.Column(db.Integer, nullable=False)
    total_failures_in_history = db.Column(db.Integer, nullable=False)

    last_maintenance_date = db.Column(db.Date, nullable=False)
    total_maintenance_activities_in_past_year = db.Column(db.Integer, nullable=False)
    maintenance_type = db.Column(db.String(60), nullable=True)
    cost_per_maintenance_activity = db.Column(db.Numeric(10, 2), nullable=True)
    total_maintenance_costs_in_past_year = db.Column(db.Numeric(10, 2), nullable=True)

    upcoming_maintenance_action_date = db.Column(db.Date, nullable=True)


class Messages(db.Model):
    __tablename__ = 'Messages'
    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # subject = db.Column(db.String(255))
    # body = db.Column(db.Text)
    # date_sent = db.Column(db.Date)
    # time_sent = db.Column(db.Time)
    sender = db.Column(db.String(25), nullable=False)
    recipient = db.Column(db.String(25), nullable=False)
    notification_send_date = db.Column(db.Date, nullable=False)
    notification_head = db.Column(db.String(35), nullable=False)
    notification_body = db.Column(db.String(160), nullable=True)

class Activity(db.Model):
    __tablename__ = 'Activities'
    activity_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text)
    type = db.Column(db.String(25))
    frequency = db.Column(db.String(50))
    date = db.Column(db.Date)
    time = db.Column(db.Time)

class ActivityAssetUser(db.Model):
    __tablename__ = 'Activities_Assets_Users'
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('Activities.activity_id'), primary_key=True)
    asset_id = db.Column(db.String(30), db.ForeignKey('Assets.asset_id'), primary_key=True)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    notes = db.Column(db.Text)

class Role(db.Model):
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(25), nullable=False)

    def define_permissions(self):
        self.create_new_users = False
        self.access_asset_info = False
        self.access_team_info = False
        self.update_teams_schedules = False
