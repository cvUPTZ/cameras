# Theft Detection Backend

This is the backend service for the theft detection system, implementing computer vision using Roboflow with ngrok integration.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and fill in your credentials:
   ```bash
   cp .env.example .env
   ```

4. Get your ngrok auth token:
   - Sign up at https://ngrok.com
   - Copy your auth token from the dashboard
   - Add it to .env as NGROK_AUTH_TOKEN

5. Start the server:
   ```bash
   python server.py
   ```

## API Endpoints

- POST `/analyze`: Analyze a frame for theft detection
- GET `/health`: Health check endpoint

The server will output the public ngrok URL that can be used to access these endpoints.