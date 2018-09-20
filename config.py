# Create dummy secrey key so we can use sessions
SECRET_KEY = '123456790'

"""
postgres_db = {'drivername': 'postgres',
               'username': 'postgres',
               'password': 'postgres',
               'host': '192.168.99.100',
               'port': 5432}
"""

# Create in-memory database
DATABASE_FILE = 'car.sqlite'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_FILE
#SQLALCHEMY_ECHO = True

# Flask-Security config
SECURITY_URL_PREFIX = "/admin"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

# Flask-Security URLs, overridden because they don't put a / at the end
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"

SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"
SECURITY_POST_REGISTER_VIEW = "/admin/"

# Flask-Security features
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

# logar pelo atributo username
SECURITY_USER_IDENTITY_ATTRIBUTES = ('username','email')


SECURITY_MSG_EMAIL_ALREADY_ASSOCIATED = (
    'E-mail [%(email)s] está associada a outra conta.',
    'error'
)
SECURITY_MSG_INVALID_EMAIL_ADDRESS = (
    'E-mail inválido.',
    'error'
)

