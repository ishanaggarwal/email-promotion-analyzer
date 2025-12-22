# 📝 Examples

This directory contains example scripts demonstrating how to use the Email Promotion Analyzer API.

## Available Examples

### `api_usage.py`

A comprehensive example showing how to interact with all API endpoints.

**What it demonstrates:**
- Health check endpoint
- Analyzing demo data
- Analyzing Gmail promotions (if configured)
- Searching for specific deals
- Real-time monitoring

**Usage:**
```bash
# Make sure the API server is running first
cd ../backend
python app.py

# In another terminal, run the example
cd examples
python api_usage.py
```

**Requirements:**
```bash
pip install requests
```

## Creating Your Own Examples

Feel free to create your own examples based on these templates. Some ideas:

- **Deal Tracker**: Monitor specific brands or products
- **Price Alert Bot**: Get notifications for high-value deals
- **Analytics Dashboard**: Visualize promotion trends
- **Email Filter**: Auto-categorize and prioritize emails
- **Deal Aggregator**: Combine deals from multiple sources

## Contributing

If you create a useful example, consider contributing it back to the project! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.
