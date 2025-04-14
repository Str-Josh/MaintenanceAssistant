from wtforms import Form, BooleanField, DateField, StringField, IntegerField, PasswordField, validators, ValidationError
import email_validator
import re


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


class RegistrationForm(Form):
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

    phone_number = IntegerField("Phone Number", [
        validators.Length(min = 7, max=10),
        validators.DataRequired(),
        
    ])

    user_role = BooleanField("Role", [
        validators.DataRequired(),
        validators.AnyOf([
            "Director", 
            "Maintenance Manager", 
            "Maintenance Staff",
        ])
    ])

    password = PasswordField('Password', [
        validators.Length(min=8, max=15),
        validate_password_strength_conditions,
        validators.DataRequired(),
    ])


class RegisterAssetForm(Form):
    device_name = StringField("Device Name", [
        validators.DataRequired(),
    ])

    brand = StringField("Brand Name", [
        validators.DataRequired(),
        validate_non_numeric_data
    ])

    generic_name = StringField("Generic Name", [
        validators.DataRequired(),
        validate_non_numeric_data
    ])

    manufacturer = StringField("Manufacturer", [
        validators.DataRequired(),
        validate_non_numeric_data
    ])

    stored_department = StringField("Stored Department", [
        validators.DataRequired(),
        validate_non_numeric_data
    ])

    installation_date = DateField("Installation Date", [
        validators.DataRequired(),
    ])