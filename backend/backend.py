import os
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# --- Groq / Llama 3 Setup ---
from groq import Groq

groq_client = Groq(api_key="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")


# --- Hugging Face Custom Model Setup ---
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# Define the repository for your fine-tuned model
model_repo = "Aygun/finetuned-distilbert-imdb"
custom_model = AutoModelForSequenceClassification.from_pretrained(model_repo)
custom_tokenizer = AutoTokenizer.from_pretrained(model_repo)

# --- FastAPI Setup ---
app = FastAPI()

# Request model for analysis endpoint
class AnalyzeRequest(BaseModel):
    text: str
    model: str  # Expected values: "Custom Model" or "Llama 3"

# Function to analyze sentiment using the custom Hugging Face model
def analyze_sentiment_custom(text: str):
    # Tokenize the text
    inputs = custom_tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = custom_model(**inputs)
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1)
        # Assuming binary classification: label 0 is negative, label 1 is positive
        sentiment_label = torch.argmax(probabilities, dim=1).item()
        confidence = probabilities[0, sentiment_label].item()
        sentiment = "positive" if sentiment_label == 1 else "negative"
    return sentiment, confidence

# Function to analyze sentiment using the Llama 3 model via Groq
def analyze_sentiment_llama3(text: str):
    # Prepare the conversation history.
    system_prompt = {
        "role": "system",
        "content": "You are a helpful assistant. You reply with very short answers."
    }
    # Here, we ask the model to analyze the sentiment of the given text.
    user_message = {
        "role": "user",
        "content": f"Analyze the sentiment of the following text: {text}"
    }
    chat_history = [system_prompt, user_message]
    
    # Call the Groq API.
    response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=chat_history,
        max_tokens=50,
        temperature=1.2
    )
    
    assistant_reply = response.choices[0].message.content

    # Naively extract sentiment and confidence from the assistant's reply.
    # (For example, the reply might be: "Sentiment: positive (Confidence: 0.95)")
    sentiment = "unknown"
    confidence = None

    if "positive" in assistant_reply.lower():
        sentiment = "positive"
    elif "negative" in assistant_reply.lower():
        sentiment = "negative"
    
    # Use a regular expression to try to extract a confidence score.
    match = re.search(r"Confidence:\s*([0-9.]+)", assistant_reply)
    if match:
        try:
            confidence = float(match.group(1))
        except ValueError:
            confidence = None

    return sentiment, confidence

# Define the /analyze endpoint
@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text input is required.")
    
    if request.model == "Aygun Model":
        sentiment, confidence = analyze_sentiment_custom(request.text)
    elif request.model == "Llama 3":
        sentiment, confidence = analyze_sentiment_llama3(request.text)
    else:
        raise HTTPException(status_code=400, detail="Invalid model selection.")
    
    return {"sentiment": sentiment, "confidence": confidence}