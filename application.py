from flask import Flask, request, jsonify
from docx import Document
import os

application = Flask(__name__)

@application.route("/")
def test_page():
    return "This is a test page!"

@application.route('/api/webhook', methods=['POST'])
def webhook():
    data = request.json
    form_data = data['form_response']
    
    # Populate Word document template
    doc = Document('model_earth_offer_letter_teamplate.docx')
    for key, value in form_data.items():
        for paragraph in doc.paragraphs:
            if key in paragraph.text:
                paragraph.text = paragraph.text.replace(f'{{{{ {key} }}}}', value)

    # Save the populated document
    doc_path = 'populated_document.docx'
    doc.save(doc_path)
    
    return jsonify({"message": "Document created successfully", "documentPath": doc_path})

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0', port=8888)