#!/usr/bin/env python3
"""
Example API Usage Script for Email Promotion Analyzer
This script demonstrates how to interact with the API
"""

import requests
import json
from time import sleep

# API Configuration
API_BASE_URL = "http://localhost:5000"

def print_section(title):
    """Print a section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def check_health():
    """Check API health status"""
    print_section("Health Check")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        data = response.json()
        
        print(f"Status: {data.get('status')}")
        print(f"Gmail Connected: {data.get('gmail_connected')}")
        if data.get('connected_email'):
            print(f"Connected Email: {data.get('connected_email')}")
        
        return data.get('status') == 'healthy'
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure the server is running: python app.py")
        return False

def analyze_demo():
    """Analyze demo email data"""
    print_section("Analyzing Demo Data")
    
    demo_emails = """---EMAIL---
From: Amazon
Subject: Flash Sale - 50% Off Electronics
Date: 2024-01-15
Body: Limited time offer! Get 50% off all electronics. Sale expires tomorrow!

---EMAIL---
From: Best Buy
Subject: Weekend Clearance Sale
Date: 2024-01-16
Body: Final clearance! Up to 70% off. Don't miss out!"""
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            json={"emails_text": demo_emails}
        )
        
        data = response.json()
        if data.get('success'):
            analytics = data.get('data', {})
            print(f"✅ Total Emails: {analytics.get('total_emails')}")
            print(f"   Average Discount: {analytics.get('average_discount')}%")
            print(f"   Top Senders: {list(analytics.get('top_senders', {}).keys())}")
            
            critical = analytics.get('critical_deals', [])
            if critical:
                print(f"   Critical Deals: {len(critical)}")
                for deal in critical[:2]:
                    print(f"     - {deal.get('sender')}: {deal.get('discount')}% off")
        else:
            print(f"❌ Error: {data.get('error')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def analyze_gmail():
    """Analyze Gmail promotional emails"""
    print_section("Analyzing Gmail (if connected)")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/analyze-gmail",
            json={"days_back": 7, "max_emails": 20}
        )
        
        data = response.json()
        if data.get('success'):
            analytics = data.get('data', {})
            print(f"✅ Connected Email: {data.get('connected_email')}")
            print(f"   Analyzed {data.get('email_count')} emails")
            print(f"   Average Discount: {analytics.get('average_discount')}%")
            
            critical = analytics.get('critical_deals', [])
            if critical:
                print(f"   🔥 {len(critical)} Critical Deals Found!")
                for deal in critical[:3]:
                    print(f"     - {deal.get('sender')}: {deal.get('discount')}% off")
                    print(f"       Expires in: {deal.get('expires_in_days')} days")
        else:
            print(f"⚠️  {data.get('error', 'Gmail not connected')}")
            print("   Tip: Add credentials.json to enable Gmail features")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def search_deals():
    """Search for specific deals"""
    print_section("Searching for Deals")
    
    search_terms = ["electronics", "clothing"]
    
    for term in search_terms:
        print(f"\nSearching for: {term}")
        try:
            response = requests.post(
                f"{API_BASE_URL}/search-gmail",
                json={"query": term}
            )
            
            data = response.json()
            if data.get('success'):
                results = data.get('results', [])
                count = data.get('count', 0)
                print(f"  ✅ Found {count} results")
                
                for result in results[:2]:
                    print(f"    - {result.get('sender')}: {result.get('subject')[:50]}...")
            else:
                print(f"  ⚠️  {data.get('error', 'No results')}")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        sleep(0.5)  # Rate limiting

def monitor_realtime():
    """Monitor real-time deals (last 24 hours)"""
    print_section("Real-time Monitoring (Last 24h)")
    
    try:
        response = requests.get(f"{API_BASE_URL}/realtime-monitor")
        data = response.json()
        
        if data.get('success'):
            print(f"✅ Latest Emails: {data.get('latest_emails')}")
            
            urgent = data.get('urgent_deals', [])
            if urgent:
                print(f"   🚨 {len(urgent)} Urgent Deals:")
                for deal in urgent[:3]:
                    print(f"     - {deal.get('sender')}: {deal.get('subject')[:50]}")
            else:
                print("   No urgent deals in the last 24 hours")
        else:
            print(f"⚠️  {data.get('error', 'Not available')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function to run all examples"""
    print("\n" + "="*60)
    print("  🤖 Email Promotion Analyzer - API Examples")
    print("="*60)
    print("\nThis script demonstrates various API endpoints.")
    print("Make sure the server is running: python app.py")
    print("\nStarting in 2 seconds...")
    sleep(2)
    
    # Check if API is running
    if not check_health():
        print("\n❌ API is not running. Please start it first:")
        print("   cd backend && python app.py")
        return
    
    # Run examples
    analyze_demo()
    analyze_gmail()
    search_deals()
    monitor_realtime()
    
    # Summary
    print_section("Summary")
    print("✅ API examples completed!")
    print("\nNext steps:")
    print("  - Check README.md for full API documentation")
    print("  - Set up Gmail integration for more features")
    print("  - Build your own application using the API")
    print("\nHappy deal hunting! 🎉\n")

if __name__ == "__main__":
    main()
