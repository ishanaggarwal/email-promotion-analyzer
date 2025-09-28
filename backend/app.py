from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from email_analyzer import EmailAnalyzer
from ai_classifier import AIClassifier
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize analyzers
email_analyzer = EmailAnalyzer()
ai_classifier = AIClassifier()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/analyze', methods=['POST'])
def analyze_emails():
    try:
        # Get email data from request
        data = request.json
        emails_text = data.get('emails_text', '')
        
        # If no text provided, use sample data
        if not emails_text:
            with open('../data/sample_emails.txt', 'r') as f:
                emails_text = f.read()
        
        # Parse emails
        emails = email_analyzer.parse_emails(emails_text)
        
        # Classify using AI
        classified_emails = ai_classifier.classify_promotions(emails)
        
        # Generate analytics
        analytics = email_analyzer.generate_analytics(classified_emails)
        
        return jsonify({
            "success": True,
            "data": analytics
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/search', methods=['POST'])
def semantic_search():
    try:
        data = request.json
        query = data.get('query', '')
        
        results = ai_classifier.semantic_search(query)
        
        return jsonify({
            "success": True,
            "results": results
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)