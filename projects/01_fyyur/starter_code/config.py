import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
# dialect = 'postgresql'
# username = ''
# password = ''
# host = 'localhost'
# port = '5432'
# database = ''
# SQLALCHEMY_DATABASE_URI = f'{dialect}://{username}:{password}@{host}:{port}/{database}'

# Another way to handle environment variables
DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_NAME = os.getenv('DB_NAME', 'your_db')

SQLALCHEMY_DATABASE_URI= 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)