import os
import json
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()


genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)


model = genai.GenerativeModel(
    "gemini-3.1-flash-lite"
)


def understand_message(message):

    prompt = f"""
        You are an egg farm management assistant.

        Convert the user message into JSON.

        Possible intents:

        - add_production
        - add_broken
        - add_sold
        - get_summary
        - get_production
        - get_broken
        - get_sold

        Return ONLY JSON.

        Required fields:

        intent
        shed
        quantity
        date

        Examples:

        User:
        "Shed 1 produced 100 eggs"

        Note : 1 tray contains 30 eggs , when the user enters in trays , you need to convert those into eggs . For example , 10 trays = 10 * 30 = 300 days 

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

        User:
        "How many broken eggs in shed 1?
"
        JSON:
        {{
            "intent":"get_broken",
            "shed":1,
            "quantity":null,
            "date":null
        }}

        User:
        "How many sold eggs in shed 2?"

        JSON:
        {{
            "intent":"get_sold",
            "shed":2,
            "quantity":null,
            "date":null
        }}

        User:
        "How many eggs were produced in shed 3?"

        JSON:
        {{
            "intent":"get_production",
            "shed":3,
            "quantity":null,
            "date":null
        }}

        Now convert this:

        {message}
        """
    response = model.generate_content(prompt)

    text = response.text.strip()

    # Remove markdown if present
    text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)