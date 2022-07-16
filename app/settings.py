import os 

# Get env variables
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SECRET_KEY = os.environ.get('SECRET_KEY')


# Ensure templates are auto-reloaded
TEMPLATES_AUTO_RELOAD = True

# Configure session to use filesystem (instead of signed cookies)
SESSION_PERMANENT = False
SESSION_TYPE = "filesystem"

SQLALCHEMY_TRACK_MODIFICATIONS = False