import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
dialect = 'postgresql'
username = ''
password = ''
host = 'localhost'
port = '5432'
database = ''
SQLALCHEMY_DATABASE_URI = f'{dialect}://{username}:{password}@{host}:{port}/{database}'

