import os
import json
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()


genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)


model = genai.GenerativeModel(
    "gemini-2.0-flash"
)


def understand_message(message):

    prompt = f"""
        You are an egg farm management assistant.

        Convert the user message into JSON.

        Possible intents:

        - add_production
        - add_broken
        - add_sold
        - query_summary

        Return ONLY JSON.

        Required fields:

        intent
        shed
        quantity
        date

        Examples:

        User:
        "Shed 1 produced 100 eggs"

        JSON:
        {{
        "intent":"add_production",
        "shed":1,
        "quantity":100
        }}

        User:
        "100 eggs are added to first shed"

        JSON:
        {{
        "intent":"add_production",
        "shed":1,
        "quantity":100
        }}

        Now convert this:

        {message}
        """
    
    response = model.generate_content(prompt)

    text = response.text.strip()

    return json.loads(text)