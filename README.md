<a style="float:right" href="https://docs.google.com/forms/d/e/1FAIpQLScXSX0_myDcB4_Z32hpGC71PXVsMmgy_dyZPY0aPEWamyzV-w/viewform" class="btn btn-success">New Member Signup</a>

# Webhook

[Our membership page](/community/members) welcome letter uses a [Flask webhook app](https://github.com/modelEarth/webhook) that runs in Google App Engine. The webhook merges member fields from our [Google Form](https://docs.google.com/forms/d/e/1FAIpQLScXSX0_myDcB4_Z32hpGC71PXVsMmgy_dyZPY0aPEWamyzV-w/viewform) into our Word Doc welcome template. The merged welcome letter Word Doc is sent to new members using MailTrap's free outbound email plan, which sends up to 200 emails per day.  <a href="https://github.com/modelearth/webhook/">GitHub</a>

Our SMTP secrets reside in Google Cloud Secret Manager. We securely store the secrets for the email service and import them into our Flask application through Cloud Computing Services (GCP).

For our Flask app's use of MailTrap outbound email, we added CNAME and TXT records to our registered domain in [Cloudflare](../../../localsite/start/cloudflare/). The&nbsp;setup requires turning off Proxy on the CNAME records.

To test, in `settings.py`, uncomment the ENV:TEST section and comment out ENV:PROD.


## Local Dev Setup

1. Run in the webhook foler to activate a virtual env for Python:

        python3.11 -m venv env
        source venv/bin/activate    # On Windows run: .\env\Scripts\activate

2. Install the packages

        pip install -r requirements.txt

Our notes on changing your Python version using [pyenv](https://model.earth/io/coders/python/)


### Local Form Data Tests Setup

To run API tests using Postman, follow [this guide](https://blog.postman.com/how-to-access-google-apis-using-oauth-in-postman/) to set up OAuth 2.0 in Postman for Google Form APIs.

The scope should be set to `https://www.googleapis.com/auth/forms.responses.readonly  https://www.googleapis.com/auth/forms.body.readonly` with a newline as the separator.

## How to Deploy GitHub Repo to Google App Engine

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


## To Create your Own Copy

1. Optionally create a private repository on GitHub, or a secure environment variable
2. Clone your repo to your local machine `git clone [YOUR_PRIVATE_REPO_GIT]`
3. `cd [YOUR_REPO]`
4. Add the original webhook repo as a remote: `git remote add upstream https://github.com/ModelEarth/webhook.git`
5. Fetch and merge changes from the original repo: `git fetch upstream` \ `git merge upstream/main`
6. Push changes to Your Repo: `git push origin main`

## Google Form

Copy the function from existing [Google Form](https://docs.google.com/forms/d/e/1FAIpQLScXSX0_myDcB4_Z32hpGC71PXVsMmgy_dyZPY0aPEWamyzV-w/viewform) by choosing "Script editor" from the 3-dots menu in upper right.

Also add the same config under "Add Trigger".

