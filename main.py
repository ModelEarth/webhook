from flask import Flask, request, jsonify
from docx import Document
import os
import re
from docx.shared import Pt
from flask_mail import Mail, Message
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
    '#jobTitle#': '19'
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

    # replace placeholders
    pattern = re.compile(r'#\w+#')
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            if run.text in placeholders:
                to_replace = ''
                if placeholders[run.text] in response:
                    to_replace = response[placeholders[run.text]]['answer'][0]
                    if run.text == '#name#':
                        first_name, full_name = to_camel_case(response['0']['answer'][0])
                        to_replace = ' '.join(full_name)
                run.text = re.sub(pattern, to_replace, run.text)
                run.font.name = 'Calibri'
                run.font.size = Pt(11)
  
    file_name = f"{''.join(full_name)}-ModelEarth-WelcomeLetter.docx"
    doc_path = os.path.join('/tmp', file_name)
    doc.save(doc_path)

    try:
        send_email(file_name, doc_path, first_name, response['13']['answer'][0])
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
    else:
        return jsonify({'status': 'success', 'documentPath': doc_path}), 200

def send_email(file_name: str, doc_path: str, first_name: str, email: str) -> None:
    with app.open_resource('outbound/new-member.txt') as tmp_body:
        msg_body = tmp_body.read().decode('utf-8')
        msg_body = msg_body.replace('[FirstName]', first_name)

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