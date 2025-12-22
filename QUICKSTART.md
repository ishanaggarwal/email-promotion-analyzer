# 🚀 Quickstart Guide

Get up and running with Email Promotion Analyzer in 5 minutes!

## Option 1: Quick Setup (Recommended)

### Linux/Mac
```bash
# Clone and run setup
git clone https://github.com/ishanaggarwal/email-promotion-analyzer.git
cd email-promotion-analyzer
./setup.sh
```

### Windows
```cmd
# Clone and run setup
git clone https://github.com/ishanaggarwal/email-promotion-analyzer.git
cd email-promotion-analyzer
setup.bat
```

## Option 2: Manual Setup

### 1. Install Dependencies
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install packages
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key (optional)
```

### 3. Run the Application
```bash
cd backend
python app.py
```

The server will start at **http://localhost:5000** 🎉

## Testing the API

### Health Check
```bash
curl http://localhost:5000/health
```

### Demo Mode (No Gmail Required)
```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"emails_text": "From: Amazon\nSubject: 50% Off Sale"}'
```

## Enabling Gmail Integration (Optional)

### 1. Get Gmail API Credentials
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download credentials as `credentials.json`

### 2. Place Credentials
```bash
# Move credentials to backend folder
mv ~/Downloads/credentials.json backend/
```

### 3. Authenticate
```bash
# Run the app - it will open a browser for OAuth
python app.py
```

### 4. Use Gmail Features
```bash
# Analyze your Gmail promotions
curl -X POST http://localhost:5000/analyze-gmail \
  -H "Content-Type: application/json" \
  -d '{"days_back": 30, "max_emails": 50}'
```

## 🎯 What's Next?

- Explore the [Full Documentation](README.md)
- Check out the [API Reference](README.md#-api-documentation)
- Read [Contributing Guidelines](CONTRIBUTING.md)

## 💡 Tips

- **No OpenAI API key?** The app uses rule-based classification as fallback
- **No Gmail?** Use demo mode to test features
- **Issues?** Check the [Troubleshooting](README.md#-troubleshooting) section

---

Happy deal hunting! 🎉
