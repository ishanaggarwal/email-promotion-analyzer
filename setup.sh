#!/bin/bash

# Email Promotion Analyzer - Quick Setup Script
# This script helps you set up the Email Promotion Analyzer quickly

set -e

echo "================================================"
echo "  Email Promotion Analyzer - Setup Script"
echo "================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✅ Found Python $PYTHON_VERSION${NC}"

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo -e "${RED}❌ Please run this script from the project root directory${NC}"
    exit 1
fi

# Create virtual environment
echo ""
echo "Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠️  Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate 2>/dev/null

# Install dependencies
echo ""
echo "Installing dependencies..."
cd backend
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo -e "${GREEN}✅ Dependencies installed${NC}"

# Create .env file if it doesn't exist
echo ""
cd ..
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✅ Created .env file from template${NC}"
    echo -e "${YELLOW}⚠️  Please edit .env and add your API keys${NC}"
else
    echo -e "${YELLOW}⚠️  .env file already exists${NC}"
fi

# Check for credentials.json
echo ""
if [ ! -f "backend/credentials.json" ]; then
    echo -e "${YELLOW}⚠️  Gmail credentials not found${NC}"
    echo "   To enable Gmail integration:"
    echo "   1. Go to https://console.cloud.google.com/"
    echo "   2. Create OAuth credentials for Gmail API"
    echo "   3. Download credentials.json to backend/ directory"
else
    echo -e "${GREEN}✅ Gmail credentials found${NC}"
fi

# Summary
echo ""
echo "================================================"
echo "  Setup Complete! 🎉"
echo "================================================"
echo ""
echo "Next steps:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate  (Linux/Mac)"
echo "     venv\\Scripts\\activate      (Windows)"
echo ""
echo "  2. Edit .env file with your API keys"
echo ""
echo "  3. Run the application:"
echo "     cd backend"
echo "     python app.py"
echo ""
echo "  4. Access the API at http://localhost:5000"
echo ""
echo "For more information, see README.md"
echo ""

exit 0
