from flask import Flask, request, jsonify
from docx import Document
import os
import re
from docx.shared import Pt
from flask_mail import Mail, Message
import datetime
app = Flask(__name__)

app.config.from_pyfile('settings.py')

mail = Mail(app)

placeholders={
    '#name#': '0',
    '#handle#': '1',
    '#team#': '2',
    '#focus#': '3',
    '#goal#': '4',
    '#schoolDegree#': '5', #optional
    '#degreeDate#': '6', #optional
    '#optDepartment#': '7', #optional
    '#optContact#': '8', #optional
    '#workingHours#': '9',
    '#location#': '10',
    '#status#': '11',
    '#github#': '12',
    '#email#': '13',
    '#phone#': '14', #optional
    '#startDate#': '15',
    '#endDate#': '16', #optional,
    '#website#': '17', #optional,
    '#note#': '18', #optional,
    '#jobTitle#': '19',
    '#todaysDate#': 'todaysDate'
}
# If numbers are added before 13 above, also update send_email() from 13 below.

@app.route("/")
def main():
    return "You've arrived at our Model.Earth webhook test page."

@app.route('/signup', methods=['POST'])
def webhook():
    response = request.json
    doc = Document('files/YourName-ModelEarth-WelcomeLetter.docx')
    first_name = ''
    full_name = ''
    todays_date = datetime.datetime.now().strftime("%B %-d, %Y")

    # Process name data upfront to ensure full_name is available
    if '0' in response:
        first_name, full_name = to_camel_case(response['0']['answer'][0])
    
    # Process GitHub data upfront to extract account name and build full path
    github_account = ''
    github_path = ''
    if '12' in response:
        github_value = response['12']['answer'][0]
        # Extract account name from various GitHub URL formats
        if github_value:
            # Remove protocol and domain if present
            if github_value.startswith('https://github.com/'):
                github_account = github_value.replace('https://github.com/', '').split('/')[0]
            elif github_value.startswith('http://github.com/'):
                github_account = github_value.replace('http://github.com/', '').split('/')[0]
            elif github_value.startswith('github.com/'):
                github_account = github_value.replace('github.com/', '').split('/')[0]
            elif github_value.startswith('/'):
                github_account = github_value.lstrip('/').split('/')[0]
            else:
                # Assume it's just the account name
                github_account = github_value.split('/')[0]
            
            # Build full GitHub path
            github_path = f"https://github.com/{github_account}"
    
    # replace placeholders in paragraphs
    def replace_in_paragraph(paragraph):
        has_changes = False
        
        for placeholder, key in placeholders.items():
            if placeholder in paragraph.text:
                to_replace = ''
                if placeholder == '#todaysDate#':
                    to_replace = todays_date
                elif key in response:
                    to_replace = response[key]['answer'][0]
                    if placeholder == '#name#':
                        to_replace = ' '.join(full_name)
                
                # Replace placeholder while preserving formatting
                for run in paragraph.runs:
                    if placeholder in run.text:
                        # Store original formatting
                        is_bold = run.bold
                        font_name = run.font.name
                        font_size = run.font.size
                        
                        # Replace text
                        run.text = run.text.replace(placeholder, to_replace)
                        
                        # Restore formatting
                        run.bold = is_bold
                        run.font.name = font_name or 'Calibri'
                        run.font.size = font_size or Pt(11)
                        has_changes = True
    
    # Replace in document paragraphs
    for paragraph in doc.paragraphs:
        replace_in_paragraph(paragraph)
    
    # Replace in table cells
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    replace_in_paragraph(paragraph)
  
    file_name = f"{''.join(full_name)}-ModelEarth-WelcomeLetter.docx"
    doc_path = os.path.join('/tmp', file_name)
    doc.save(doc_path)

    try:
        send_email(file_name, doc_path, first_name, response['13']['answer'][0], github_path)
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
    else:
        return jsonify({'status': 'success', 'documentPath': doc_path}), 200

def send_email(file_name: str, doc_path: str, first_name: str, email: str, github_path: str) -> None:
    with app.open_resource('outbound/new-member.txt') as tmp_body:
        msg_body = tmp_body.read().decode('utf-8')
        msg_body = msg_body.replace('[FirstName]', first_name)
        msg_body = msg_body.replace('[githubPath]', github_path)

        msg = Message(
            subject="Welcome to our model.earth team!",
            recipients=[email],
            cc=[app.config['MAIL_DEFAULT_SENDER']]
        )
        msg.body = msg_body
        with app.open_resource(doc_path) as f:
            msg.attach(
                file_name, 
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                f.read()
            )
            mail.send(msg)

def to_camel_case(name: str) -> list[str, list[str]]:
    parts = name.split()
    camel_case_parts = [part.capitalize() for part in parts]
    return camel_case_parts[0], camel_case_parts

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)