from os import environ
MAIL_USERNAME = environ.get('MAIL_USERNAME')
MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
MAIL_PORT = '2525'
MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_DEFAULT_SENDER = ('from@example.com')