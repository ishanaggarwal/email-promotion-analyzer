from flask import Flask, request, jsonify, @app.route('/health', methods=['GET', 'OPTIONS'])
def health():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
        return response
        
    return jsonify({
        "status": "healthy",
        "gmail_connected": gmail is not None and gmail.service is not None if gmail_available else False,
        "connected_email": gmail.user_email if gmail and hasattr(gmail, 'user_email') else None
    }), 200sponse
from flask_cors import CORS
import json
from email_analyzer import EmailAnalyzer
from ai_classifier import AIClassifier
import os
from dotenv import load_dotenv

# Import Gmail connector
try:
    from gmail_connector import GmailConnector
    gmail_available = True
    gmail = None
except ImportError:
    gmail_available = False
    print("Gmail connector not available. Install google-auth packages to enable.")

load_dotenv()

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000", "http://localhost:5000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialize analyzers
email_analyzer = EmailAnalyzer()
ai_classifier = AIClassifier()

# Try to initialize Gmail if available
if gmail_available:
    try:
        gmail = GmailConnector()
        if not gmail.service:
            gmail = None
            print("Gmail authentication failed. Gmail features will be disabled.")
    except Exception as e:
        print(f"Could not initialize Gmail: {str(e)}")
        gmail = None

@app.route('/auth/google')
def auth_google():
    flow = Flow.from_client_secrets_file(
        'credentials.json',
        scopes=SCOPES,
        redirect_uri='http://localhost:5000/oauth2callback'
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    flow = Flow.from_client_secrets_file(
        'credentials.json',
        scopes=SCOPES,
        state=session['state'],
        redirect_uri='http://localhost:5000/oauth2callback'
    )
    
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    
    return redirect('http://localhost:3000')

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'auth_configured': os.path.exists('credentials.json'),
        'authenticated': 'credentials' in session,
        'session_active': bool(session)
    }), 200
    return jsonify({
        "status": "healthy",
        "gmail_connected": gmail is not None and gmail.service is not None,
        "connected_email": gmail.user_email if gmail and gmail.user_email else None
    }), 200

@app.route('/analyze', methods=['POST'])
def analyze_emails():
    """Original analyze endpoint for demo data"""
    try:
        data = request.json
        emails_text = data.get('emails_text', '')
        
        if not emails_text:
            with open('../data/sample_emails.txt', 'r') as f:
                emails_text = f.read()
        
        emails = email_analyzer.parse_emails(emails_text)
        classified_emails = ai_classifier.classify_promotions(emails)
        analytics = email_analyzer.generate_analytics(classified_emails)
        
        return jsonify({
            "success": True,
            "data": analytics,
            "source": "demo_data"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/analyze-gmail', methods=['POST'])
def analyze_gmail():
    """Analyze real Gmail promotional emails"""
    if not gmail or not gmail.service:
        return jsonify({
            "success": False,
            "error": "Gmail not connected. Please check credentials.json"
        }), 503
    
    try:
        data = request.json
        days_back = data.get('days_back', 30)
        max_emails = data.get('max_emails', 50)
        
        print(f"📧 Fetching emails from last {days_back} days...")
        emails = gmail.get_promotional_emails(
            max_results=max_emails,
            days_back=days_back
        )
        
        if not emails:
            return jsonify({
                "success": False,
                "message": "No promotional emails found in your Gmail",
                "connected_email": gmail.user_email
            }), 404
        
        print(f"🤖 Analyzing {len(emails)} emails...")
        
        # Convert Gmail format to our analyzer format
        formatted_emails = []
        for email in emails:
            formatted_emails.append({
                'sender': email['sender'],
                'subject': email['subject'],
                'body': email['body'],
                'date': email['date']
            })
        
        # Analyze using existing analyzer
        classified_emails = ai_classifier.classify_promotions(formatted_emails)
        analytics = email_analyzer.generate_analytics(classified_emails)
        
        # Add Gmail-specific info
        analytics['connected_email'] = gmail.user_email
        analytics['source'] = 'gmail'
        
        return jsonify({
            "success": True,
            "data": analytics,
            "email_count": len(emails),
            "source": "Gmail",
            "connected_email": gmail.user_email
        }), 200
        
    except Exception as e:
        print(f"Error in analyze_gmail: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/search-gmail', methods=['POST'])
def search_gmail():
    """Search Gmail for specific deals"""
    if not gmail or not gmail.service:
        return jsonify({
            "success": False,
            "error": "Gmail not connected"
        }), 503
        
    try:
        data = request.json
        search_term = data.get('query', '')
        
        if not search_term:
            return jsonify({
                "success": False,
                "message": "Search query required"
            }), 400
        
        results = gmail.search_deals(search_term)
        
        if results:
            # Format for analysis
            formatted_emails = []
            for email in results:
                formatted_emails.append({
                    'sender': email['sender'],
                    'subject': email['subject'],
                    'body': email['body'],
                    'date': email['date']
                })
            
            # Quick analysis
            classified = ai_classifier.classify_promotions(formatted_emails[:10])
            
            return jsonify({
                "success": True,
                "results": classified,
                "count": len(results),
                "query": search_term
            }), 200
        else:
            return jsonify({
                "success": True,
                "results": [],
                "message": "No deals found matching your search"
            }), 200
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/realtime-monitor', methods=['GET'])
def realtime_monitor():
    """Get latest promotional emails (last 24 hours)"""
    if not gmail or not gmail.service:
        return jsonify({
            "success": False,
            "error": "Gmail not connected"
        }), 503
        
    try:
        emails = gmail.get_promotional_emails(
            max_results=20,
            days_back=1
        )
        
        if emails:
            formatted_emails = []
            for email in emails:
                formatted_emails.append({
                    'sender': email['sender'],
                    'subject': email['subject'],
                    'body': email['body'],
                    'date': email['date']
                })
            
            # Quick classification
            classified = ai_classifier.classify_promotions(formatted_emails)
            
            # Find urgent deals
            urgent_deals = [e for e in classified if e.get('urgency_score', 0) >= 7]
            
            return jsonify({
                "success": True,
                "latest_emails": len(emails),
                "urgent_deals": urgent_deals[:5],
                "connected_email": gmail.user_email
            }), 200
        else:
            return jsonify({
                "success": True,
                "latest_emails": 0,
                "urgent_deals": [],
                "connected_email": gmail.user_email
            }), 200
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/search', methods=['POST'])
def semantic_search():
    """Original semantic search endpoint"""
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
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   🤖 AI Email Promotion Analyzer API                 ║
    ║   With Gmail Integration Support                      ║
    ╚══════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=5000, debug=True)
    
    if gmail and gmail.service:
        print(f"    ✅ Gmail Connected: {gmail.user_email}")
    else:
        print("    ⚠️  Gmail not connected - using demo mode")
        print("    📝 To enable Gmail: place credentials.json in backend folder")
    
    print("""
    Available endpoints:
    - GET  /health           → Check API status
    - POST /analyze          → Analyze demo emails
    - POST /analyze-gmail    → Analyze your Gmail (if connected)
    - POST /search-gmail     → Search Gmail for deals
    - GET  /realtime-monitor → Check latest Gmail deals (24h)
    - POST /search           → Semantic search
    
    Press Ctrl+C to stop the server
    """)
    
    app.run(debug=True, port=5000)