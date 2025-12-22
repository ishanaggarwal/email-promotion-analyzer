"""Gmail Connector for Email Promotion Analyzer"""
import os
import base64
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_AUTH_AVAILABLE = True
except ImportError:
    GOOGLE_AUTH_AVAILABLE = False
    print("Google authentication libraries not available. Install with: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")


class GmailConnector:
    """Connect to Gmail and fetch promotional emails"""
    
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    def __init__(self, credentials_file: str = 'credentials.json', token_file: str = 'token.json'):
        """Initialize Gmail connector with OAuth credentials"""
        if not GOOGLE_AUTH_AVAILABLE:
            raise ImportError("Google authentication libraries not installed")
            
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        self.user_email = None
        
        # Authenticate
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Gmail API using OAuth2"""
        creds = None
        
        # The file token.json stores the user's access and refresh tokens
        if os.path.exists(self.token_file):
            try:
                creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)
            except Exception as e:
                print(f"Error loading token: {e}")
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing token: {e}")
                    creds = None
            
            if not creds:
                if not os.path.exists(self.credentials_file):
                    print(f"Credentials file {self.credentials_file} not found")
                    return
                
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, self.SCOPES)
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    print(f"Error during authentication: {e}")
                    return
            
            # Save the credentials for the next run
            if creds:
                try:
                    with open(self.token_file, 'w') as token:
                        token.write(creds.to_json())
                except Exception as e:
                    print(f"Error saving token: {e}")
        
        try:
            # Build the Gmail service
            self.service = build('gmail', 'v1', credentials=creds)
            
            # Get user email address
            profile = self.service.users().getProfile(userId='me').execute()
            self.user_email = profile.get('emailAddress', 'Unknown')
            
            print(f"✅ Successfully connected to Gmail: {self.user_email}")
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            self.service = None
    
    def get_promotional_emails(self, max_results: int = 50, days_back: int = 30) -> List[Dict]:
        """
        Fetch promotional emails from Gmail
        
        Args:
            max_results: Maximum number of emails to fetch
            days_back: Number of days to look back
            
        Returns:
            List of email dictionaries with sender, subject, body, date
        """
        if not self.service:
            print("Gmail service not initialized")
            return []
        
        try:
            # Calculate date filter
            date_from = datetime.now() - timedelta(days=days_back)
            date_str = date_from.strftime('%Y/%m/%d')
            
            # Search for promotional emails
            query = f'category:promotions after:{date_str}'
            
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                print("No promotional emails found")
                return []
            
            print(f"Found {len(messages)} promotional emails")
            
            # Fetch full message details
            emails = []
            for msg in messages:
                email_data = self._get_message_details(msg['id'])
                if email_data:
                    emails.append(email_data)
            
            return emails
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []
    
    def _get_message_details(self, msg_id: str) -> Optional[Dict]:
        """Get detailed information about a specific message"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=msg_id,
                format='full'
            ).execute()
            
            # Extract headers
            headers = message['payload'].get('headers', [])
            sender = self._get_header(headers, 'From')
            subject = self._get_header(headers, 'Subject')
            date_str = self._get_header(headers, 'Date')
            
            # Parse date
            try:
                # Simple date parsing - you might want to use dateutil.parser for better parsing
                date = datetime.now()
            except:
                date = datetime.now()
            
            # Extract body
            body = self._get_message_body(message['payload'])
            
            return {
                'id': msg_id,
                'sender': sender,
                'subject': subject,
                'body': body[:1000],  # Limit body length
                'date': date,
                'date_str': date_str
            }
            
        except HttpError as error:
            print(f"An error occurred fetching message {msg_id}: {error}")
            return None
    
    def _get_header(self, headers: List[Dict], name: str) -> str:
        """Extract a specific header value"""
        for header in headers:
            if header['name'].lower() == name.lower():
                return header['value']
        return ''
    
    def _get_message_body(self, payload: Dict) -> str:
        """Extract message body from payload"""
        body = ''
        
        if 'parts' in payload:
            # Multipart message
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        break
                elif part['mimeType'] == 'text/html' and not body:
                    if 'data' in part['body']:
                        # Use HTML if plain text not available
                        html_body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        # Remove HTML tags (simple approach)
                        body = re.sub('<[^<]+?>', '', html_body)
        else:
            # Single part message
            if 'data' in payload.get('body', {}):
                body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        
        return body.strip()
    
    def search_deals(self, search_term: str, max_results: int = 20) -> List[Dict]:
        """
        Search for specific deals in promotional emails
        
        Args:
            search_term: Term to search for (e.g., "electronics", "50% off")
            max_results: Maximum number of results
            
        Returns:
            List of matching emails
        """
        if not self.service:
            return []
        
        try:
            query = f'category:promotions {search_term}'
            
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            emails = []
            for msg in messages:
                email_data = self._get_message_details(msg['id'])
                if email_data:
                    emails.append(email_data)
            
            return emails
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []
    
    def get_email_count(self) -> int:
        """Get total count of promotional emails"""
        if not self.service:
            return 0
        
        try:
            results = self.service.users().messages().list(
                userId='me',
                q='category:promotions',
                maxResults=1
            ).execute()
            
            return results.get('resultSizeEstimate', 0)
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return 0
