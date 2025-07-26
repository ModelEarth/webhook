from google.cloud import secretmanager

PROJECT_ID='rock-objective-431022-a3'

############ ENV:TEST ##################
# MAIL_USERNAME = '2f02ebc7b1c93e'
# MAIL_PORT = '2525' 
# MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
# SECRET_ID = 'mailtrap_password_test'
########################################

############ ENV:PROD ##################
SECRET_ID = 'mailtrap_password_prod'
MAIL_SERVER = 'live.smtp.mailtrap.io'
MAIL_PORT = '587' 
MAIL_USERNAME = 'api'
########################################

MAIL_DEFAULT_SENDER = 'loren@dreamstudio.com'
MAIL_USE_TLS = True
MAIL_USE_SSL = False

# Get the mailtrap password using the SECRET_ID in Google Cloud
def get_secret(secret_id: str, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"

    response = client.access_secret_version(name=name) 
    return response.payload.data.decode('UTF-8')

MAIL_PASSWORD = get_secret(SECRET_ID)
