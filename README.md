<div align="center">

# 🎯 Email Promotion Analyzer

### AI-Powered Email Promotion Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![AI Powered](https://img.shields.io/badge/AI-Powered-purple.svg)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Never miss a great deal again!** Automatically analyze, classify, and extract insights from your promotional emails using advanced AI and machine learning.

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [API](#-api-documentation) • [Contributing](#-contributing)

</div>

---

## 🌟 Overview

Email Promotion Analyzer is an intelligent system that connects to your Gmail account, automatically categorizes promotional emails, and uses AI to identify the best deals, urgency levels, and personalized recommendations. Say goodbye to cluttered inboxes and missed opportunities!

### Why Email Promotion Analyzer?

- 📊 **Smart Analytics**: Get instant insights on your promotional emails
- 🤖 **AI Classification**: Advanced machine learning categorizes promotions automatically
- ⚡ **Urgency Detection**: Never miss time-sensitive deals
- 🔍 **Semantic Search**: Find specific deals using natural language
- 📧 **Gmail Integration**: Direct integration with your Gmail account
- 🎯 **Deal Scoring**: AI-powered value and urgency scoring

---

## ✨ Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| 🔗 **Gmail Integration** | Seamless OAuth2 connection to fetch promotional emails |
| 🧠 **AI Classification** | Categorize promotions (flash sales, BOGO, clearance, etc.) |
| 📈 **Analytics Dashboard** | Comprehensive statistics and insights |
| 🔎 **Semantic Search** | Find deals using natural language queries |
| ⏰ **Real-time Monitoring** | Track latest deals from the last 24 hours |
| 💎 **Deal Scoring** | AI-powered urgency and value scoring |
| 📊 **Vector Database** | ChromaDB for efficient similarity search |
| 🎨 **REST API** | Full-featured API for integration |

### Advanced Features

- **Discount Extraction**: Automatically extract percentage discounts from email content
- **Expiry Detection**: Identify time-limited offers and deadlines
- **Sender Analytics**: Track which brands send the most promotions
- **Promotion Type Distribution**: Understand your promotional email landscape
- **Critical Deals Alerts**: Highlighted deals expiring soon with high discounts
- **Batch Processing**: Analyze multiple emails efficiently

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Gmail account (optional, for Gmail integration)
- OpenAI API key (optional, for enhanced AI features)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ishanaggarwal/email-promotion-analyzer.git
   cd email-promotion-analyzer
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp ../.env.example .env
   # Edit .env and add your OpenAI API key (optional)
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

The server will start at `http://localhost:5000` 🎉

---

## 🎮 Usage

### Basic Usage (Without Gmail)

Start with the demo mode to test the analyzer:

```bash
python app.py
```

The API will be available with demo data analysis capabilities.

### Gmail Integration Setup

To enable Gmail integration for analyzing real emails:

1. **Create Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one

2. **Enable Gmail API**
   - Navigate to "APIs & Services" > "Library"
   - Search for "Gmail API" and enable it

3. **Create OAuth Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app" as application type
   - Download the credentials JSON file

4. **Configure Application**
   - Rename the downloaded file to `credentials.json`
   - Place it in the `backend/` directory

5. **First Run Authentication**
   ```bash
   cd backend
   python app.py
   ```
   - A browser window will open for OAuth authentication
   - Grant the necessary permissions
   - You'll see: ✅ Successfully connected to Gmail

### Making API Requests

#### Analyze Gmail Promotions
```bash
curl -X POST http://localhost:5000/analyze-gmail \
  -H "Content-Type: application/json" \
  -d '{"days_back": 30, "max_emails": 50}'
```

#### Search for Specific Deals
```bash
curl -X POST http://localhost:5000/search-gmail \
  -H "Content-Type: application/json" \
  -d '{"query": "electronics 50% off"}'
```

#### Check Latest Deals (24h)
```bash
curl http://localhost:5000/realtime-monitor
```

#### Health Check
```bash
curl http://localhost:5000/health
```

---

## 📚 API Documentation

### Endpoints

#### `GET /health`
Check API status and Gmail connection.

**Response:**
```json
{
  "status": "healthy",
  "gmail_connected": true,
  "connected_email": "your.email@gmail.com"
}
```

#### `POST /analyze-gmail`
Analyze promotional emails from your Gmail account.

**Request Body:**
```json
{
  "days_back": 30,
  "max_emails": 50
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "total_emails": 150,
    "average_discount": 35.5,
    "promotion_types": {
      "flash_sale": 45,
      "percentage_off": 60,
      "clearance": 25
    },
    "top_senders": {
      "Amazon": 30,
      "Best Buy": 25
    },
    "critical_deals": [
      {
        "sender": "Nike",
        "subject": "Flash Sale: 50% Off Everything",
        "discount": 50,
        "expires_in_days": 1,
        "urgency_score": 9
      }
    ]
  },
  "source": "Gmail",
  "connected_email": "your.email@gmail.com"
}
```

#### `POST /search-gmail`
Search for specific deals in Gmail promotions.

**Request Body:**
```json
{
  "query": "electronics discount"
}
```

**Response:**
```json
{
  "success": true,
  "results": [...],
  "count": 15,
  "query": "electronics discount"
}
```

#### `GET /realtime-monitor`
Get latest promotional emails from the last 24 hours.

**Response:**
```json
{
  "success": true,
  "latest_emails": 10,
  "urgent_deals": [...],
  "connected_email": "your.email@gmail.com"
}
```

#### `POST /analyze`
Analyze demo/custom email data (without Gmail).

**Request Body:**
```json
{
  "emails_text": "Your email content here..."
}
```

#### `POST /search`
Perform semantic search on stored emails.

**Request Body:**
```json
{
  "query": "laptop deals under $1000"
}
```

---

## 🏗️ Architecture

### Technology Stack

**Backend:**
- **Flask**: Web framework
- **Python 3.8+**: Core language
- **OpenAI API**: AI-powered classification (optional)
- **Sentence Transformers**: Local embeddings generation
- **ChromaDB**: Vector database for semantic search
- **Google APIs**: Gmail integration

**AI/ML Components:**
- **all-MiniLM-L6-v2**: Sentence embeddings model
- **Pattern Matching**: Rule-based classification
- **Vector Similarity**: Semantic search capabilities

### Project Structure

```
email-promotion-analyzer/
├── backend/
│   ├── app.py                  # Main Flask application
│   ├── email_analyzer.py       # Email parsing and analytics
│   ├── ai_classifier.py        # AI classification engine
│   ├── gmail_connector.py      # Gmail API integration
│   ├── simple_app.py          # Simple demo server
│   ├── test_gmail.py          # Gmail connection test
│   └── requirements.txt       # Python dependencies
├── .env.example              # Environment configuration template
├── .gitignore               # Git ignore rules
├── LICENSE                  # MIT License
└── README.md               # This file
```

### Data Flow

```
Gmail API → Email Fetcher → Parser → AI Classifier → Analytics Engine → REST API
                                           ↓
                                    Vector Database
                                    (Semantic Search)
```

---

## 🎯 Use Cases

1. **Deal Hunters**: Find the best discounts across all your promotional emails
2. **Budget Shoppers**: Track promotions from favorite brands
3. **Time Savers**: Quickly identify urgent, expiring deals
4. **Data Analysts**: Analyze promotional email trends
5. **Developers**: Build custom applications on top of the API

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory (copy from `.env.example`):

```env
# OpenAI API Key (optional, for enhanced AI features)
OPENAI_API_KEY=your_openai_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Server Configuration
HOST=0.0.0.0
PORT=5000
```

### Gmail API Setup

1. Obtain `credentials.json` from Google Cloud Console
2. Place in `backend/` directory
3. Run the application - it will guide you through OAuth
4. A `token.json` file will be created for future sessions

---

## 🧪 Testing

### Test Gmail Connection

```bash
cd backend
python test_gmail.py
```

### Run the Demo Server

```bash
cd backend
python simple_app.py
```

Access at `http://localhost:8000`

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Add docstrings to all functions and classes
- Update documentation for new features
- Test your changes thoroughly
- Keep commits atomic and well-described

---

## 🐛 Troubleshooting

### Common Issues

**Gmail not connecting**
- Ensure `credentials.json` is in the `backend/` directory
- Delete `token.json` and re-authenticate
- Check that Gmail API is enabled in Google Cloud Console

**Missing dependencies**
```bash
pip install -r backend/requirements.txt --upgrade
```

**ChromaDB errors**
- Delete the `chroma_db/` directory and restart
- Ensure sufficient disk space

**OpenAI API errors**
- Verify your API key in `.env`
- Check your OpenAI account has credits
- The app works without OpenAI (uses rule-based classification)

---

## 📈 Roadmap

- [ ] Web-based UI dashboard
- [ ] Support for other email providers (Outlook, Yahoo)
- [ ] Machine learning model training on user preferences
- [ ] Email filtering and auto-categorization
- [ ] Browser extension
- [ ] Mobile app
- [ ] Advanced analytics and visualizations
- [ ] Multi-language support
- [ ] Deal price tracking over time

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI** for GPT models
- **Google** for Gmail API
- **Hugging Face** for Sentence Transformers
- **ChromaDB** for vector database
- All the amazing open-source contributors

---

## 📞 Support

- 📧 Email: [Create an issue](https://github.com/ishanaggarwal/email-promotion-analyzer/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/ishanaggarwal/email-promotion-analyzer/discussions)
- 🐛 Bug Reports: [GitHub Issues](https://github.com/ishanaggarwal/email-promotion-analyzer/issues)

---

<div align="center">

**Made with ❤️ for deal hunters everywhere**

⭐ **Star this repo** if you find it helpful!

[Back to Top](#-email-promotion-analyzer)

</div>
