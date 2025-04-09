import os

base_directory = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = "TESTSECRETKEY"

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(base_directory, "database.db")

