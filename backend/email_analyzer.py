import re
import pandas as pd
from datetime import datetime, timedelta
from collections import Counter
import json

class EmailAnalyzer:
    def __init__(self):
        self.promotion_patterns = {
            'flash_sale': r'flash|limited time|today only|ends tonight',
            'percentage_off': r'\d+%\s*off|\d+\s*percent',
            'bogo': r'buy one get|bogo|b1g1',
            'free_shipping': r'free shipping|free delivery',
            'clearance': r'clearance|final sale|last chance'
        }
    
    def parse_emails(self, text):
        """Parse raw text into structured email data"""
        emails = []
        
        # Simple parsing - in production, use more sophisticated methods
        # Split by common email separators
        email_blocks = text.split('---EMAIL---')
        
        for block in email_blocks:
            if block.strip():
                email = self.extract_email_info(block)
                if email:
                    emails.append(email)
        
        return emails
    
    def extract_email_info(self, email_text):
        """Extract structured info from email text"""
        lines = email_text.strip().split('\n')
        
        email_data = {
            'sender': '',
            'subject': '',
            'body': '',
            'date': datetime.now(),
            'discount': None,
            'expiry': None
        }
        
        # Extract sender (look for From: pattern)
        for line in lines:
            if line.startswith('From:'):
                email_data['sender'] = line.replace('From:', '').strip()
            elif line.startswith('Subject:'):
                email_data['subject'] = line.replace('Subject:', '').strip()
            elif line.startswith('Date:'):
                try:
                    email_data['date'] = datetime.strptime(
                        line.replace('Date:', '').strip(), 
                        '%Y-%m-%d'
                    )
                except:
                    email_data['date'] = datetime.now()
        
        # Rest is body
        body_start = False
        body_lines = []
        for line in lines:
            if body_start:
                body_lines.append(line)
            elif line.startswith('Body:'):
                body_start = True
                body_lines.append(line.replace('Body:', '').strip())
        
        email_data['body'] = ' '.join(body_lines)
        
        # Extract discount
        discount_match = re.search(r'(\d+)%\s*off', email_data['body'], re.IGNORECASE)
        if discount_match:
            email_data['discount'] = int(discount_match.group(1))
        
        # Extract expiry (simple pattern matching)
        if 'expires' in email_data['body'].lower():
            # Try to find date after "expires"
            email_data['expiry'] = datetime.now() + timedelta(days=2)
        
        return email_data
    
    def generate_analytics(self, emails):
        """Generate comprehensive analytics from classified emails"""
        
        # Basic stats
        total_emails = len(emails)
        
        # Promotion type distribution
        promotion_types = Counter([e.get('promotion_type', 'other') for e in emails])
        
        # Top senders
        senders = Counter([e['sender'] for e in emails])
        top_senders = dict(senders.most_common(5))
        
        # Time-critical deals (expires in next 48 hours)
        critical_deals = []
        for email in emails:
            if email.get('expiry'):
                days_until = (email['expiry'] - datetime.now()).days
                if 0 <= days_until <= 2 and email.get('discount', 0) >= 30:
                    critical_deals.append({
                        'sender': email['sender'],
                        'subject': email['subject'],
                        'discount': email['discount'],
                        'expires_in_days': days_until,
                        'urgency_score': email.get('urgency_score', 5)
                    })
        
        # Average discount
        discounts = [e['discount'] for e in emails if e.get('discount')]
        avg_discount = sum(discounts) / len(discounts) if discounts else 0
        
        return {
            'total_emails': total_emails,
            'promotion_types': dict(promotion_types),
            'top_senders': top_senders,
            'critical_deals': sorted(critical_deals, key=lambda x: x['expires_in_days'])[:10],
            'average_discount': round(avg_discount, 1),
            'date_range': {
                'start': min([e['date'] for e in emails]).isoformat() if emails else None,
                'end': max([e['date'] for e in emails]).isoformat() if emails else None
            }
        }