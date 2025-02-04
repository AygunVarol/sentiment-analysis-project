import reactpy
from reactpy import component, html, hooks
import asyncio
import httpx  # For making asynchronous HTTP requests (optional)

# Replace with your actual backend endpoint URL
BACKEND_API_URL = "http://localhost:5000/analyze"

@component
def SentimentAnalyzer():
    # State for user input text
    text_input, set_text_input = hooks.use_state("")
    # State for the selected model from the dropdown
    selected_model, set_selected_model = hooks.use_state("Aygun Model")
    # State for the result from the backend API
    result, set_result = hooks.use_state("")

    # Handler for text input change
    def handle_text_change(event):
        set_text_input(event["target"]["value"])

    # Handler for dropdown selection change
    def handle_model_change(event):
        set_selected_model(event["target"]["value"])

    # Handler for button click that calls the backend API
    async def analyze_sentiment(event):
        if not text_input.strip():
            set_result("Please enter some text to analyze.")
            return

        # Create the payload to send to your API
        payload = {
            "text": text_input,
            "model": selected_model,
        }

        try:
            # Use an async HTTP client to post the data.
            # Make sure your backend API is running and configured to accept these requests.
            async with httpx.AsyncClient() as client:
                response = await client.post(BACKEND_API_URL, json=payload)
                response.raise_for_status()
                data = response.json()
                # Expected response structure:
                # {
                #    "sentiment": "positive" or "negative",
                #    "confidence": 0.95  # optional
                # }
                sentiment = data.get("sentiment", "unknown")
                confidence = data.get("confidence", None)
                if confidence is not None:
                    set_result(f"Sentiment: {sentiment} (Confidence: {confidence:.2f})")
                else:
                    set_result(f"Sentiment: {sentiment}")
        except Exception as e:
            set_result(f"Error analyzing sentiment: {str(e)}")

    return html.div(
        {"style": {"fontFamily": "Arial, sans-serif", "maxWidth": "600px", "margin": "auto", "padding": "20px"}},
        html.h1("Sentiment Analyzer"),
        html.div(
            {"style": {"marginBottom": "10px"}},
            html.label({"for": "text-input"}, "Enter text:"),
            html.input({
                "id": "text-input",
                "type": "text",
                "value": text_input,
                "on_change": handle_text_change,
                "style": {"width": "100%", "padding": "8px", "marginTop": "5px"}
            })
        ),
        html.div(
            {"style": {"marginBottom": "10px"}},
            html.label({"for": "model-select"}, "Select model:"),
            html.select({
                "id": "model-select",
                "value": selected_model,
                "on_change": handle_model_change,
                "style": {"width": "100%", "padding": "8px", "marginTop": "5px"}
            },
                html.option({"value": "Aygun Model"}, "Aygun Model"),
                html.option({"value": "Llama 3"}, "Llama 3")
            )
        ),
        html.button({
            "on_click": analyze_sentiment,
            "style": {"padding": "10px 20px", "cursor": "pointer"}
        }, "Analyze Sentiment"),
        html.div(
            {"style": {"marginTop": "20px", "padding": "10px", "backgroundColor": "#f0f0f0"}},
            result
        )
    )

# Run the ReactPy app
if __name__ == "__main__":
    reactpy.run(SentimentAnalyzer)