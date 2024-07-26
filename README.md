# How to Set up 
## Local Dev Setup
1. Activate virtual env for Python: \
    `python3 -m venv venv`\
    `source venv/bin/activate`
2. Install the packages \
   `pip install -r requirements.txt`

### Local Form Data Tests Setup
In order to do some local tests on Postman, please follow [this guide](https://blog.postman.com/how-to-access-google-apis-using-oauth-in-postman/) to set up OAuth 2.0 in Postman for Google Form APIs.

The scope should be set to `https://www.googleapis.com/auth/forms.responses.readonly  https://www.googleapis.com/auth/forms.body.readonly` with a newline as the separator.