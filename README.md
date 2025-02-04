# Sentiment Analysis Project

This project implements a sentiment analysis system using a fine-tuned transformer model and a Llama 3 model accessed via Groq Cloud API. The project includes:
- A Jupyter Notebook for data preprocessing, model fine-tuning, and uploading to Hugging Face.
- A backend API built with FastAPI to serve the sentiment analysis.
- A simple React UI for user interaction.

## Table of Contents
- [Installation](#installation)
- [Running the Notebook](#running-the-notebook)
- [Running the Backend API](#running-the-backend-api)
- [Using the Endpoints](#using-the-endpoints)
- [UI Explanation](#ui-explanation)
- [License](#license)

## Installation

### Prerequisites
- Python 3.8 or later
- Node.js and npm (for the React UI)

### Python Dependencies
1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
   
2. Install the required Python packages for the notebook and API:

    ```bash
    pip install -r backend/requirements.txt
   ```

3. Node.js Dependencies (UI)
   
    ```bash
    cd ui
    npm install
   ```

4. Running the Backend API

    ```bash
    cd backend
    uvicorn main:app --reload
   ```
   The API will start locally at http://127.0.0.1:8000

5. Testing with curl

Custom Model
  ```bash
curl -X POST "http://127.0.0.1:8000/analyze/" \
     -H "Content-Type: application/json" \
     -d '{"text": "This movie was fantastic!", "model": "custom"}'
   ```

Llama Model
  ```bash
curl -X POST "http://127.0.0.1:8000/analyze/" \
     -H "Content-Type: application/json" \
     -d '{"text": "This movie was terrible.", "model": "llama"}'
   ```

6. Testing with Python requests

  ```bash
import requests

url = "http://127.0.0.1:8000/analyze/"

payload = {
  "text": "This movie was fantastic!",
  "model": "custom"
}

response = requests.post(url, json=payload)
print(response.json())
   ```

7. Run UI Locally

  ```bash
npm start
   ```
