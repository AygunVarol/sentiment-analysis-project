# Sentiment Analysis Project

This project implements a sentiment analysis system using a fine-tuned transformer model and a Llama 3 model accessed via Groq Cloud API. The project includes:
- A Jupyter Notebook for data preprocessing, model fine-tuning, and uploading to Hugging Face.
- A backend API built with FastAPI to serve the sentiment analysis.
- A simple React UI for user interaction.

## [HuggingFace Model](https://huggingface.co/Aygun/finetuned-distilbert-imdb)

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
    
3. Running the Backend API

    ```bash
    cd backend
    uvicorn backend:app --reload --port 8000
   ```
   The API will start locally at http://127.0.0.1:8000

4. Run UI Locally

     ```bash
      python reactUIdesign.py
      ```
