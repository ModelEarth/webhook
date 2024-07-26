from flask import Flask, request, jsonify
from docx import Document
import os

application = Flask(__name__)

@application.route("/")
def test_page():
    return "This is a test page!"

@application.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    doc = Document()
    doc.add_heading('Form Response', level=1)

    # Extracting answers
    for question_id, answer_data in data['answers'].items():
        question_answers = [answer['value'] for answer in answer_data['textAnswers']['answers']]
        doc.add_paragraph(f"Question ID {question_id}: {', '.join(question_answers)}")

    doc_path = os.path.join('generated_docs', 'FormData.docx')
    if not os.path.exists('generated_docs'):
        os.makedirs('generated_docs')
    doc.save(doc_path)

    return jsonify({'status': 'success', 'documentPath': doc_path}), 200

if __name__ == '__main__':
    application.run(debug=True, host='127.0.0.1', port=8000)