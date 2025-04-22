# Form Validation

from wtforms import Form, SelectField, DateField, StringField, IntegerField, PasswordField, validators, ValidationError
from flask_wtf import FlaskForm

import email_validator
import re

DEMO = True  # Determines if we use every validation or not.


def validate_non_numeric_data(form, field):
    if any(char.isdigit() for char in field.data):
        raise ValidationError("Field cannot contain numbers.")
    

def validate_only_numeric_data(form, field):
    if any(char.isnumeric() for char in field.data):
        raise ValidationError("Field must be only numbers")


def validate_password_strength_conditions(form, field):
    password = field.data
    number_special_characters = re.findall(r'[!@#$%^&*(),.?":{}|<>]', password)
    
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not re.search(r'\d', password):
        raise ValidationError("Password must contain at least one number.")
    if len(number_special_characters) < 1:
        raise ValidationError("Password must contain at least one special character.")


class RegistrationForm(FlaskForm):
    username = StringField('Username', [
        validators.Length(min=4, max=25),
        validators.DataRequired(),
        validate_non_numeric_data
    ])

    first_name = StringField("First Name", [
        validators.Length(min=2, max=15),
        validators.DataRequired(),
        validate_non_numeric_data
    ])

    last_name = StringField("Last Name", [
        validators.Length(min=2, max=25),
        validators.Optional(),
        validate_non_numeric_data
    ])

    email = StringField('Email Address', [
        validators.Length(min=6, max=35),
        validators.Email(),
        validators.DataRequired()  # ensures there exists context
    ])

    phone_number = StringField("Phone Number", [
        validators.Length(min = 7, max=11),
        validators.DataRequired(),
    ])

    user_role = SelectField("Role", choices=[
        ("Director", "Director"),
        ("Manager", "Maintenance Manager"),
        ("Staff", "Maintenance Staff"),
    ], 
    validators=[
        validators.DataRequired(),
    ])

    if DEMO:
        password = PasswordField('Password', [
            validators.Length(min=8, max=15),
            # validate_password_strength_conditions,
            validators.DataRequired(),
        ])
    else:  # SET DEMO = FALSE TO VALIDATE PASSWORD STRENGTH
        password = PasswordField('Password', [
            validators.Length(min=8, max=15),
            validate_password_strength_conditions,
            validators.DataRequired(),
        ])


class RegisterAssetForm(FlaskForm):
    device_name = StringField("Device Name", [
        validators.DataRequired(),
    ])

    brand_name = StringField("Brand Name", [
        validators.DataRequired(),
        validate_non_numeric_data
    ])

    generic_name = StringField("Generic Name", [
        validators.DataRequired(),
        validate_non_numeric_data
    ])

    manufacturer_name = StringField("Manufacturer", [
        validators.DataRequired(),
        validate_non_numeric_data
    ])

    home_dept_location = StringField("Stored Department", [
        validators.DataRequired(),
        validate_non_numeric_data
    ])

    installation_date = DateField("Installation Date", [
        validators.DataRequired(),
    ])

    average_uses_per_year = StringField("Average Uses Per Year", [
        validators.DataRequired(),
        validate_only_numeric_data
    ])

    maintenance_activities_year = StringField("Total Maintenance Activities Last Year", [
        validators.DataRequired(),
    ])

    common_maintenance_activity = StringField("Common Maintenance Activity", [
        validators.DataRequired(),
    ])



class TeamMemberSendMessage(FlaskForm):
    recipient_member = SelectField(
        "Receiving Team Member", 
        choices=[], 
        validators=[
            validators.DataRequired(),
        ]
    )

    message_subject = StringField("Message Subject", [
        validators.DataRequired(),
        validators.Length(max=35),
    ])

    message_body = StringField("Message Body", [
        # We're gonna require this even though it's nullable in DB since why would they just send subject, it'll be fine. It's not that deep
        validators.DataRequired(),
        validators.Length(max=160)
    ])


class ReplyMemberMessage(FlaskForm):
    message_subject = StringField("Message Subject", [
        validators.DataRequired(),
        validators.Length(max=35),
    ])

    message_body = StringField("Message Body", [
        # We're gonna require this even though it's nullable in DB since why would they just send subject, it'll be fine. It's not that deep
        validators.DataRequired(),
        validators.Length(max=160)
    ])


class SearchAssetForm(FlaskForm):
    search_by = SelectField(
        "Search By",
        choices=[
            ("serial_number", "Serial Number"),
            ("generic_name", "Generic Name"),
            ("manufacturer", "Manufacturer"),
            ("brand", "Brand Name"),
            ("department", "Department Location"),
            # ("Upcoming Maintenance Date", "Upcoming Maintenance Date"),
            ("last_maintenance_date", "Last Maintenance Date"),
        ],
        validators=[
            validators.DataRequired()
        ]
    )

    search_phrase = StringField("Search Phrase", [
        validators.DataRequired(),
        validators.Length(max=75)  # assuming you wouldn't need more than 75 characters.. Right???
    ])
