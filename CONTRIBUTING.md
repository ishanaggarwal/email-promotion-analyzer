# Contributing to Email Promotion Analyzer

Thank you for your interest in contributing to Email Promotion Analyzer! We welcome contributions from everyone.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment (OS, Python version, etc.)
- Any relevant logs or screenshots

### Suggesting Features

We love new ideas! To suggest a feature:
- Check if it's already been suggested in the issues
- Create a new issue with the "enhancement" label
- Clearly describe the feature and its benefits
- Explain how it should work

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Commit your changes** with clear, descriptive messages
6. **Push to your fork** and submit a pull request

#### Coding Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code
- Add docstrings to all functions, classes, and modules
- Keep functions small and focused
- Write meaningful variable names
- Comment complex logic
- Add type hints where appropriate

#### Testing

- Test your changes before submitting a PR
- Ensure existing functionality still works
- Add tests for new features if possible

#### Commit Messages

Write clear, concise commit messages:
- Use the imperative mood ("Add feature" not "Added feature")
- Keep the first line under 50 characters
- Add detailed description if needed

Example:
```
Add semantic search for promotional emails

- Implement vector embedding generation
- Add ChromaDB integration for similarity search
- Update API endpoint documentation
```

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ishanaggarwal/email-promotion-analyzer.git
   cd email-promotion-analyzer
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp ../.env.example .env
   # Edit .env with your configuration
   ```

5. Run the application:
   ```bash
   python app.py
   ```

## Project Structure

```
email-promotion-analyzer/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── email_analyzer.py   # Email parsing and analytics
│   ├── ai_classifier.py    # AI classification engine
│   ├── gmail_connector.py  # Gmail API integration
│   └── requirements.txt    # Dependencies
├── .env.example           # Environment template
├── .gitignore            # Git ignore rules
├── LICENSE               # MIT License
├── README.md            # Main documentation
└── CONTRIBUTING.md      # This file
```

## Need Help?

- 📧 Create an issue for questions
- 💬 Use GitHub Discussions for general questions
- 🐛 Report bugs via GitHub Issues

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Respect differing opinions
- Keep discussions professional

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Email Promotion Analyzer! 🎉
