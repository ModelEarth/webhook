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
    '#schoolDegree#': '4', #optional
    '#degreeDate#': '5', #optional
    '#optDepartment#': '6', #optional
    '#optContact#': '7', #optional
    '#workingHours#': '8',
    '#github#': '11',
    '#phone#': '12', #optional
    '#email#': '13',
    '#startDate#': '14',
    '#endDate#': '15', #optional
}

@app.route("/")
def main():
    return "You arrievd Model.Earth Webhook test page"

@app.route('/signup', methods=['POST'])
def webhook():
    response = request.json
    doc = Document('offer_letter_template.docx')
    
    # replace placeholders
    pattern = re.compile(r'#\w+#')
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            if run.text in placeholders:
                to_replace = ''
                if placeholders[run.text] in response:
                    to_replace = response[placeholders[run.text]]['answer'][0]
                run.text = re.sub(pattern, to_replace, run.text)
                run.font.name = 'Calibri'
                run.font.size = Pt(11)
  
    file_name = f"{response['0']['answer'][0]}_Offer_Letter.docx"
    doc_path = os.path.join('/tmp', file_name)
    doc.save(doc_path)

    try:
        send_email(file_name, doc_path)
    except Exception:
        return jsonify({'status': 'failure', 'documentPath': doc_path}), 500
    else:
        return jsonify({'status': 'success', 'documentPath': doc_path}), 200

def send_email(file_name, doc_path):
    msg = Message(
        subject="Test Hello",
        recipients=['to@example.com'],
        cc=['loren@dreamstudio.com']
    )
    msg.body = "this is a test email"
    with app.open_resource(doc_path) as f:
        msg.attach(
            file_name, 
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            f.read()
        )
        mail.send(msg)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)