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

def translate_response(message, language):

    if language == "en":
        return message

    prompt = f"""
    Translate the following message into the language code '{language}'.

    Rules:
    - Keep all numbers exactly the same.
    - Preserve emojis.
    - Translate words like "Shed", "Produced", "Broken", "Sold", "Stock".
    - Do not change the shed number.
    - Return only the translated text.

    Message:
    {message}
    """

    response = model.generate_content(prompt)

    return response.text.strip()

def understand_message(message):

    prompt = f"""
        You are an egg farm management assistant.

        If the user wants to add production, broken, or sold eggs but does not specify a shed number, return:

        {{
            "intent":"add_production",
            "shed":null,
            "quantity":10,
            "date":"today", 
            "language":"en"
        }}

        Do not guess the shed number.

        Convert the user message into JSON.

        User:
        11-07-2026 summary

        JSON:
        {{
            "intent":"get_daily_summary",
            "shed":null,
            "quantity":null,
            "date":"2026-07-11", 
            "language":"en"
        }}

        User:
        11 July 2026 summary

        JSON:
        {{
        "intent":"get_daily_summary",
        "shed":null,
        "quantity":null,
        "date":"2026-07-11", 
        "language":"en"
        }}

        Possible intents:

        - add_production
        - add_broken
        - add_sold
        - get_summary
        - get_production
        - get_broken
        - get_sold
        - get_daily_summary
        - get_remaining


        Return ONLY JSON.

        Required fields:

        intent
        shed
        quantity
        date

        Important Rules:

        1. If the user mentions a shed number (e.g., Shed 1, Shed 2, first shed), use the shed-specific intents:
        - get_summary
        - get_production
        - get_broken
        - get_sold

        2. If the user does NOT mention any shed number and asks for today's summary, yesterday's summary, or a daily report, use:
        - get_daily_summary

        Examples:

        User:
        "Shed 1 produced 100 eggs"

        Note : 1 tray contains 30 eggs , when the user enters in trays , you need to convert those into eggs . For example , 10 trays = 10 * 30 = 300 days 

        JSON:
        {{
        "intent":"add_production",
        "shed":1,
        "quantity":100, 
        "language":"en"
        }}

        User:
        "100 eggs are added to first shed"

        JSON:
        {{
        "intent":"add_production",
        "shed":1,
        "quantity":100, 
        "language":"en"
        }}

        User:
        "How many broken eggs in shed 1?
"
        JSON:
        {{
            "intent":"get_broken",
            "shed":1,
            "quantity":null,
            "date":null, 
            "language":"en"
        }}

        User:
        "How many sold eggs in shed 2?"

        JSON:
        {{
            "intent":"get_sold",
            "shed":2,
            "quantity":null,
            "date":null, 
            "language":"en"
        }}

        User:
        "How many eggs were produced in shed 3?"

        JSON:
        {{
            "intent":"get_production",
            "shed":3,
            "quantity":null,
            "date":null, 
            "language":"en"
        }}

        User:
        Today's summary

        JSON:
        {{
            "intent":"get_daily_summary",
            "shed":null,
            "quantity":null,
            "date":"today", 
            "language":"en"
        }}

        User:
        Yesterday's summary

        JSON:
        {{
            "intent":"get_daily_summary",
            "shed":null,
            "quantity":null,
            "date":"yesterday", 
            "language":"en"
        }}

        User:
        Yesterday shed 1 summary

        JSON:
        {{
            "intent":"get_summary",
            "shed":1,
            "quantity":null,
            "date":"yesterday", 
            "language":"en"
        }}

        User:
        Today shed 2 summary

        JSON:
        {{
            "intent":"get_summary",
            "shed":2,
            "quantity":null,
            "date":"today", 
            "language":"en"
        }}

        User:
        Remaining eggs in shed 1

        JSON:
        {{
            "intent":"get_remaining",
            "shed":1,
            "quantity":null,
            "date":"today", 
            "language":"en"
        }}

        User:
        Remaining eggs in shed 1 yesterday

        JSON:
        {{
            "intent":"get_remaining",
            "shed":1,
            "quantity":null,
            "date":"yesterday" ,
            "language":"en"
        }}

        Now convert this:

        {message}
        """
    response = model.generate_content(prompt)

    text = response.text.strip()

    # Remove markdown if present
    text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)