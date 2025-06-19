# Email Summarization Agent

This agent fetches newsletters from your Microsoft Outlook account, summarizes them, and sends you a daily brief.

## Setup Instructions

1. **Prerequisites**
   - Python 3.10 or higher
   - Microsoft Outlook account
   - Poetry (Python package manager)
   - Ollama (for local LLM inference)

2. **Installation**
   ```bash
   # Install Poetry if you haven't already
   pip install poetry

   # Install Ollama
   # For Windows: Download from https://ollama.ai/download
   # For Linux/Mac:
   curl -fsSL https://ollama.ai/install.sh | sh

   # Pull the Mistral model
   ollama pull mistral

   # Install dependencies
   poetry install
   ```

3. **Configuration**
   Create a `.env` file in the root directory with the following variables:
   ```
   OUTLOOK_CLIENT_ID=your_client_id
   SENDER_EMAIL=your_email@outlook.com
   ```

4. **Microsoft Azure Setup**
   - Register an application in Azure Portal
   - Grant necessary permissions (Mail.Read, Mail.Send)
   - Get the client ID, client secret, and tenant ID

5. **Running the Agent**
   ```bash
   poetry run python src/main.py
   ```

## Features
- Daily newsletter fetching
- AI-powered summarization using local LLM (Mistral)
- Automated daily brief delivery
- Configurable newsletter filters

## Project Structure
```
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── email_client.py
│   ├── summarizer.py
│   └── scheduler.py
├── config/
│   └── settings.py
├── pyproject.toml
└── README.md
```
