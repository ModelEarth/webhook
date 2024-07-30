from google.cloud import secretmanager

MAIL_USERNAME = 'f15ffc0a8d06b2'
PROJECT_ID='upheld-chalice-430519-n5'
MAIL_PORT = '2525'
MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_DEFAULT_SENDER = ('from@example.com')

def get_secret(secret_id: str, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"

    response = client.access_secret_version(name=name) 
    return response.payload.data.decode('UTF-8')

MAIL_PASSWORD = get_secret('mailtrap_password')
