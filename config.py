import os

base_directory = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = "TESTSECRETKEY"

CACHE_TYPE = "SimpleCache"

CACHE_DEFAULT_TIMEOUT = 400

# SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(base_directory, "database.db")

