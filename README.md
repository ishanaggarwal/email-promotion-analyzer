# AI-Powered Email Promotion Analyzer

An intelligent email analyzer that uses AI, semantic search, and vector embeddings to extract insights from promotional emails.

## Features :)

- **AI Classification**: Uses transformer models to classify promotion types
- **Semantic Search**: Vector embeddings with ChromaDB for intelligent search
- **Time-Critical Detection**: AI identifies urgent deals
- **Smart Analytics**: ML-powered insights and recommendations
- **Real-time Dashboard**: Interactive visualization of email analytics

## Tech Stack

### Backend
- Python 3.9+
- Flask (REST API)
- OpenAI API (GPT-4 for classification)
- Sentence Transformers (embeddings)
- ChromaDB (vector database)
- SpaCy (NLP)

### Frontend
- React 18
- Recharts (data visualization)
- Axios (API calls)

## Installation

### 1. Clone Repository
\`\`\`bash
git clone <your-repo-url>
cd email-promotion-analyzer
\`\`\`

### 2. Backend Setup
\`\`\`bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
\`\`\`

### 3. Environment Variables
Create `.env` file in backend folder:
\`\`\`
OPENAI_API_KEY=your_openai_api_key_here
PORT=5000
\`\`\`

### 4. Frontend Setup
\`\`\`bash
cd ../frontend
npm install
\`\`\`

## Running the Application

### Start Backend (Terminal 1)
\`\`\`bash
cd backend
source venv/bin/activate
python app.py
\`\`\`

### Start Frontend (Terminal 2)
\`\`\`bash
cd frontend
npm start
\`\`\`

Visit: http://localhost:3000

## Architecture

### AI Pipeline
1. **Email Parsing**: Extract structured data from raw text
2. **Embedding Generation**: Convert emails to vector representations
3. **AI Classification**: Use transformers to categorize promotions
4. **Vector Storage**: Store in ChromaDB for semantic search
5. **Analytics Generation**: ML-powered insights

### Key Components
- **EmailAnalyzer**: Processes and structures email data
- **AIClassifier**: Handles AI/ML operations
- **Vector Database**: Enables semantic search
- **React Dashboard**: Interactive visualization

## API Endpoints

- `POST /analyze`: Analyze email text
- `POST /search`: Semantic search
- `GET /health`: Health check

## Interview Talking Points

1. **AI-First Approach**: Leveraged modern AI tools for rapid development
2. **Semantic Understanding**: Goes beyond keyword matching
3. **Scalability**: Vector DB handles millions of emails efficiently
4. **Modern Stack**: Latest AI/ML technologies
5. **Production Ready**: Error handling, logging, and testing

## Future Enhancements

- Gmail API integration
- Real-time email monitoring
- Personalized recommendations
- Advanced NLP with GPT-4
- Fraud detection
- Export functionality

## License

MIT
