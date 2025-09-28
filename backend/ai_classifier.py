import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import openai
from typing import List, Dict
import json

class AIClassifier:
    def __init__(self):
        # Initialize OpenAI
        openai.api_key = os.getenv('OPENAI_API_KEY', '')
        
        # Initialize sentence transformer for embeddings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB for vector storage
        self.chroma_client = chromadb.Client(Settings(
            persist_directory="./chroma_db",
            anonymized_telemetry=False
        ))
        
        # Create or get collection
        try:
            self.collection = self.chroma_client.create_collection(
                name="promotions",
                metadata={"hnsw:space": "cosine"}
            )
        except:
            self.collection = self.chroma_client.get_collection("promotions")
    
    def classify_promotions(self, emails: List[Dict]) -> List[Dict]:
        """Classify emails using AI"""
        classified_emails = []
        
        for email in emails:
            # Generate embedding
            embedding = self.model.encode(email['body'])
            
            # Classify using AI (simplified for demo)
            classification = self._classify_single_email(email)
            
            # Add to email data
            email.update(classification)
            
            # Store in vector DB
            self._store_in_vectordb(email, embedding)
            
            classified_emails.append(email)
        
        return classified_emails
    
    def _classify_single_email(self, email: Dict) -> Dict:
        """Use AI to classify a single email"""
        
        # For demo, use rule-based classification
        # In production, use OpenAI API
        
        text = f"{email['subject']} {email['body']}".lower()
        
        classification = {
            'promotion_type': 'general',
            'urgency_score': 5,
            'value_score': 5,
            'ai_summary': ''
        }
        
        # Simple classification rules
        if 'flash' in text or 'limited time' in text:
            classification['promotion_type'] = 'flash_sale'
            classification['urgency_score'] = 9
        elif 'clearance' in text or 'final sale' in text:
            classification['promotion_type'] = 'clearance'
            classification['urgency_score'] = 7
        elif 'bogo' in text or 'buy one get' in text:
            classification['promotion_type'] = 'bogo'
            classification['value_score'] = 8
        elif '% off' in text or 'percent off' in text:
            classification['promotion_type'] = 'percentage_off'
        elif 'free shipping' in text:
            classification['promotion_type'] = 'free_shipping'
        
        # Generate AI summary (simplified)
        classification['ai_summary'] = f"Promotion from {email['sender']} offering {email.get('discount', 'special')}% discount"
        
        return classification
    
    def _store_in_vectordb(self, email: Dict, embedding):
        """Store email and embedding in vector database"""
        try:
            self.collection.add(
                embeddings=[embedding.tolist()],
                documents=[email['body']],
                metadatas=[{
                    'sender': email['sender'],
                    'subject': email['subject'],
                    'discount': str(email.get('discount', 0)),
                    'promotion_type': email.get('promotion_type', 'other')
                }],
                ids=[f"email_{email['date'].isoformat()}_{email['sender'][:10]}"]
            )
        except Exception as e:
            print(f"Error storing in vector DB: {e}")
    
    def semantic_search(self, query: str, n_results: int = 5) -> List[Dict]:
        """Perform semantic search on stored emails"""
        try:
            # Encode query
            query_embedding = self.model.encode(query)
            
            # Search in vector DB
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=n_results
            )
            
            # Format results
            formatted_results = []
            if results['metadatas']:
                for i, metadata in enumerate(results['metadatas'][0]):
                    formatted_results.append({
                        'sender': metadata.get('sender', ''),
                        'subject': metadata.get('subject', ''),
                        'discount': metadata.get('discount', '0'),
                        'promotion_type': metadata.get('promotion_type', ''),
                        'relevance_score': 1 - results['distances'][0][i]
                    })
            
            return formatted_results
            
        except Exception as e:
            print(f"Semantic search error: {e}")
            return []
    
    def get_ai_recommendations(self, user_preferences: Dict) -> List[Dict]:
        """Get AI-powered recommendations based on user preferences"""
        # This would use OpenAI API in production
        # Simplified for demo
        return []