# Our Webhook Setup 

Our webhook populates a Word Doc from a [Google Form](https://model.earth/community/members) and emails the document to our new members.

If you're testing, please uncomment the ENV:TEST section in `settings.py`.

## Getting Started

1. Optionally create a private repository on GitHub, or a secure environment variable
2. Clone your repo to your local machine `git clone [YOUR_PRIVATE_REPO_GIT]`
3. `cd [YOUR_REPO]`
4. Add the original webhook repo as a remote: `git remote add upstream https://github.com/ModelEarth/webhook.git`
5. Fetch and merge changes from the original repo: `git fetch upstream` \ `git merge upstream/main`
6. Push changes to Your Repo: `git push origin main`

## Local Dev Setup

1. Activate virtual env for Python:

        python3.11 -m venv env
        source venv/bin/activate

2. Install the packages

        pip install -r requirements.txt

### Local Form Data Tests Setup

In order to do some local tests on Postman, please follow [this guide](https://blog.postman.com/how-to-access-google-apis-using-oauth-in-postman/) to set up OAuth 2.0 in Postman for Google Form APIs.

The scope should be set to `https://www.googleapis.com/auth/forms.responses.readonly  https://www.googleapis.com/auth/forms.body.readonly` with a newline as the separator.

## How to Deploy to Google App Engine

1. Follow [Creating Your Google Cloud Project](https://cloud.google.com/appengine/docs/standard/python3/building-app/creating-gcp-project)
2. Follow [Deploying Your Web Service](https://cloud.google.com/appengine/docs/standard/python3/building-app/deploying-web-service)
3. In the terminal, run `gcloud auth application-default login` to authenticate Google CLI access.
4. Run `gcloud config set project [PROJECT_ID]`.
5. Grant Secret Manager Access to App Engine Service Account. Checkout this [guide](https://cloud.google.com/secret-manager/docs/access-control). This is used to access the SMTP password stored in Google Cloud Secret Manager.
6. Run `gcloud init` and then `gcloud app deploy`
7. The app should be deployed. Run `gcloud app browse` to see the landing test page.

## How to Set Up SMTP Service

1. Choose any SMTP email service you like: sendGrid, MailTrap, etc.
2. Follow the website's guide to create the account and set up your domain
3. One common issue if CNAME records cannot be verified. 
    [Source](https://developers.cloudflare.com/dns/manage-dns-records/troubleshooting/cname-domain-verification/) : To get verified, turn off proxy for the 4 MailTrap CNAME records. Retain "Flatten CNAME at apex", the default and only option in Cloudflare.


## Google Form

Copy the function from existing Google Form by choosing "Script editor" from the 3-dots menu in upper right.

Also add the same config under "Add Trigger".

