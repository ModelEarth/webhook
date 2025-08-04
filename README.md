<a style="float:right" href="https://docs.google.com/forms/d/e/1FAIpQLScXSX0_myDcB4_Z32hpGC71PXVsMmgy_dyZPY0aPEWamyzV-w/viewform" class="btn btn-success">New Member Signup</a>

# Webhook

[Our membership page](/community/members) welcome letter uses a [Flask webhook app](https://github.com/modelEarth/webhook) that runs in Google App Engine. The webhook merges member fields from our [Google Form](https://docs.google.com/forms/d/e/1FAIpQLScXSX0_myDcB4_Z32hpGC71PXVsMmgy_dyZPY0aPEWamyzV-w/viewform) into our Word Doc welcome template. The merged welcome letter Word Doc is sent to new members using MailTrap's free outbound email plan, which sends up to 200 emails per day.  <a href="https://github.com/modelearth/webhook/">GitHub</a>

Our SMTP secrets reside in Google Cloud Secret Manager. We securely store the secrets for the email service and import them into our Flask application through Cloud Computing Services (GCP).

For our Flask app's use of MailTrap outbound email, we added CNAME and TXT records to our registered domain in [Cloudflare](../../../localsite/start/cloudflare/). The&nbsp;setup requires turning off Proxy on the CNAME records.

To test, in `settings.py`, uncomment the ENV:TEST section and comment out ENV:PROD.


## Local Dev Setup

<!--
.python-version file contained 3.11
Probably from running:
pyenv local 3.11

        python3.11 -m venv env

Our notes on changing your Python version using [pyenv](https://model.earth/io/coders/python/)
-->

1. Run in the webhook folder to activate a virtual env for Python:

        python -m venv env
        source venv/bin/activate    # On Windows run: .\env\Scripts\activate

2. Install the packages

        pip install -r requirements.txt

<!--
There's no package.json for this
        npm ci
npm ci (clean install) is similar to npm install, but doesn't modify the package-lock.json.  
Alternatively, run: `pip install -r requirements.txt`
-->

If you receive the error `No module named 'imp'` you'll need to replace the older (python 3.11) google-cloud-cli folder in your user root by deleteing and replacing it with the latest [Google Cloud sdk folder](https://cloud.google.com/sdk/docs/install).

## How to Deploy GitHub Repo to Google App Engine

**To deploy an update:** Skip to step 6

1. Follow [Creating Your Google Cloud Project](https://cloud.google.com/appengine/docs/standard/python3/building-app/creating-gcp-project)
2. Follow [Deploying Your Web Service](https://cloud.google.com/appengine/docs/standard/python3/building-app/deploying-web-service)

<!-- gcloud app deploy -->

3. In the terminal, run `gcloud auth application-default login` to authenticate Google CLI access.
4. Run `gcloud config set project [PROJECT_ID]`.
5. Grant Secret Manager Access to App Engine Service Account.  
Checkout this [guide](https://cloud.google.com/secret-manager/docs/access-control). This is used to access the SMTP password stored in Google Cloud Secret Manager.

6. Run `gcloud init` and choose options

(numbers will change)): 
Switch to and re-initialize existing configuration: [webhook-from-member-form] (4)
Your email l.h (1) 
Your Project rock-obj... (9)  
  
<!--And ignore .boto error.-->

Lastly run `gcloud app deploy` followed by Y.


### Occasionally you'll need to update the python version in app.yaml

runtime: python311


<!--
In cmd prompt, created configuration name:
webhook-from-member-form
l h @ g mail

Ignore: Error creating a default .boto configuration file. Please run [gsutil config -n] if you would like to create this file. Because:
"In most cases, users who want to use a CLI to work with Cloud Storage should not use the gsutil tool. Instead, you should work with the Google Cloud CLI and use gcloud storage commands."
Source: https://cloud.google.com/storage/docs/gsutil_install

Why does `gcloud app deploy` upload 2031 files?

You can stream logs from the command line by running:
  $ gcloud app logs tail -s default

To terminate log streaming:
Ctrl + C

To view your application in the web browser run:
  $ gcloud app browse

You'll see:
You've arrived at the Model.Earth Webhook test page
-->

The app should be deployed. Run `gcloud app browse` to see the landing test page, which is simply the text: You've arrived at our Model.Earth webhook test page.

## Local Form Data Tests - Postman Setup

To run API tests using Postman, follow [this guide](https://blog.postman.com/how-to-access-google-apis-using-oauth-in-postman/) to set up OAuth 2.0 in Postman for Google Form APIs.

The scope should be set to `https://www.googleapis.com/auth/forms.responses.readonly  https://www.googleapis.com/auth/forms.body.readonly` with a newline as the separator.

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

On the Triggers page (fourth icon on the left), click "Add Trigger" and for Function "onSubmit" set "From Form" event type "On form submit".  You can change "notify me immediately" to "notify me daily"

